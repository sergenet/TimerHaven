import java.util.Properties
import java.io.FileInputStream

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
}

// Load local keystore properties (keystore.properties in project root).
val keystorePropsFile = rootProject.file("keystore.properties")
val keystoreProps = Properties().apply {
    if (keystorePropsFile.exists()) {
        load(FileInputStream(keystorePropsFile))
    }
}

// Read contact secret from local.properties (project root) or project properties
val contactSecret: String = run {
    val lp = rootProject.file("local.properties")
    if (lp.exists()) {
        val props = Properties().apply { load(FileInputStream(lp)) }
        props.getProperty("contactSecret")?.takeIf { it.isNotBlank() } ?: (findProperty("contactSecret")?.toString() ?: "")
    } else {
        findProperty("contactSecret")?.toString() ?: ""
    }
}

android {
    // Must exactly match the package in Play Console (case-sensitive)
    namespace = "com.sergenet.TimerHavenApp"
    compileSdk = 36
    ndkVersion = "27.1.12297006"

    defaultConfig {
        // MUST match Play Console package exactly (case-sensitive)
        applicationId = "com.sergenet.TimerHavenApp"
        minSdk = 24
        targetSdk = 36
        versionCode = 49
        versionName = "1.1.2"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        ndk {
            debugSymbolLevel = "FULL"
        }
    }

    signingConfigs {
        create("release") {
            val storeFilePath = keystoreProps.getProperty("storeFile") ?: ""
            if (storeFilePath.isNotBlank()) {
                storeFile = file(storeFilePath)
            }
            storePassword = keystoreProps.getProperty("storePassword") ?: ""
            keyAlias = keystoreProps.getProperty("keyAlias") ?: ""
            keyPassword = keystoreProps.getProperty("keyPassword") ?: ""
            val st = keystoreProps.getProperty("storeType")
            if (!st.isNullOrBlank()) {
                storeType = st
            }
        }
    }

    buildTypes {
        debug {
            // Expose contact secret in debug builds for local testing (read from local.properties)
            buildConfigField("String", "CONTACT_SECRET", "\"$contactSecret\"")
        }

        release {
            signingConfig = signingConfigs.getByName("release")
            // R8 code optimization + resource shrinking (Play's "R8 optimization" advice)
            isMinifyEnabled = true
            isShrinkResources = true

            // Add contact secret to release BuildConfig (value taken from local.properties)
            buildConfigField("String", "CONTACT_SECRET", "\"$contactSecret\"")

            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
    buildFeatures {
    compose = true
    buildConfig = true
}
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation(platform("com.google.firebase:firebase-bom:33.1.2"))
    implementation("com.google.firebase:firebase-auth-ktx")
    implementation("com.google.firebase:firebase-firestore-ktx")
    implementation("com.google.firebase:firebase-analytics-ktx")
    // Crash reporting: uncaught exceptions and ANRs from real devices land in the
    // Firebase console with device, OS and app-version context.
    implementation("com.google.firebase:firebase-crashlytics")
    implementation("com.google.android.gms:play-services-auth:20.7.0")
    implementation("com.github.PhilJay:MPAndroidChart:v3.1.0")
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    implementation("androidx.browser:browser:1.5.0")
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)

    // AdMob
    implementation("com.google.android.gms:play-services-ads:23.1.0")

    // Play Billing (ktx)
    implementation("com.android.billingclient:billing-ktx:8.0.0")

    // View-based Material components and AppCompat (required for MaterialToolbar)
    implementation("com.google.android.material:material:1.8.0")
    implementation("androidx.appcompat:appcompat:1.6.1")

    // Activity KTX (registerForActivityResult, etc.)
    implementation("androidx.activity:activity-ktx:1.9.0")

    // OkHttp for network POSTs
    implementation("com.squareup.okhttp3:okhttp:4.11.0")
}

// Automated sync: Copy web files from c:\TimerHavenWebsite to assets before build
tasks.register<Copy>("syncWebAssets") {
    from("C:/TimerHavenWebsite") {
        include("**/*.html")
        include("**/*.js")
        include("**/*.css")
        include("**/*.json")
        include("assets/img/**") 
        exclude("node_modules/**")
        exclude(".git/**")
        exclude(".idea/**")
        exclude("blog/**")
        exclude("benefits-of-taking-breaks-*.html")
        exclude("recommended-products.html")
        exclude("**/*share-image.png")
        exclude("**/*.docx")
    }
    into("src/main/assets")
    duplicatesStrategy = DuplicatesStrategy.INCLUDE
}

// tasks.named("preBuild") {
//     dependsOn("syncWebAssets")
// }

// Release guard: a release bundle is what gets uploaded to Play, so refuse to
// build one when the live listing has drifted from the fastlane copy.
val checkStoreListings by tasks.registering(Exec::class) {
    group = "verification"
    description = "Compares the fastlane store listings with the live Play listings."
    workingDir = rootProject.projectDir
    commandLine(System.getenv("PYTHON") ?: "python", "tools/check_store_listings.py")
    // Exit 2 means the check could not run at all (no Play credentials, or Play
    // refused the request), which is a skip rather than a drift.
    isIgnoreExitValue = true
    doLast {
        when (executionResult.get().exitValue) {
            0 -> Unit
            2 -> logger.warn(
                "checkStoreListings skipped: the listing could not be checked " +
                    "(set PLAY_ACCESS_TOKEN, and see the message above); uploading unverified."
            )
            else -> throw GradleException(
                "Store listing drift: fastlane and the live Play listing disagree. " +
                    "Run 'python tools/check_store_listings.py' for the differing fields."
            )
        }
    }
}

tasks.matching { it.name == "bundleRelease" || it.name == "assembleRelease" }.configureEach {
    dependsOn(checkStoreListings)
}