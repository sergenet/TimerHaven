// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    id("com.google.gms.google-services") version "4.4.2" apply false
    // Crashlytics reporting for release builds; also uploads the R8 mapping so
    // release stack traces come back readable instead of obfuscated.
    id("com.google.firebase.crashlytics") version "3.0.8" apply false
}