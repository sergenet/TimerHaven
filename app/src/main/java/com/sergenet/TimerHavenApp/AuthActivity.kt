package com.sergenet.TimerHavenApp

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase

class AuthActivity : ComponentActivity() {
    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize Firebase Auth
        auth = Firebase.auth
        
        // Check if user is already signed in
        val currentUser = auth.currentUser
        if (currentUser != null) {
            // User is signed in, go to main app
            navigateToMain()
            return
        }

        setContent {
            MaterialTheme {
                var isSignUp by remember { mutableStateOf(false) }
                
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    if (isSignUp) {
                        SignUpScreen(
                            onSignUpClick = { email, password -> signUp(email, password) },
                            onSwitchToSignIn = { isSignUp = false },
                            onGoogleSignIn = { signInWithGoogle() }
                        )
                    } else {
                        SignInScreen(
                            onSignInClick = { email, password -> signIn(email, password) },
                            onSwitchToSignUp = { isSignUp = true },
                            onGoogleSignIn = { signInWithGoogle() }
                        )
                    }
                }
            }
        }
    }

    private fun signIn(email: String, password: String) {
        if (email.isBlank() || password.isBlank()) {
            Toast.makeText(this, "Please enter email and password", Toast.LENGTH_SHORT).show()
            return
        }

        auth.signInWithEmailAndPassword(email, password)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Toast.makeText(this, "Sign in successful!", Toast.LENGTH_SHORT).show()
                    navigateToMain()
                } else {
                    Toast.makeText(this, "Sign in failed: ${task.exception?.message}", Toast.LENGTH_LONG).show()
                }
            }
    }

    private fun signUp(email: String, password: String) {
        if (email.isBlank() || password.isBlank()) {
            Toast.makeText(this, "Please enter email and password", Toast.LENGTH_SHORT).show()
            return
        }

        if (password.length < 6) {
            Toast.makeText(this, "Password must be at least 6 characters", Toast.LENGTH_SHORT).show()
            return
        }

        auth.createUserWithEmailAndPassword(email, password)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Toast.makeText(this, "Account created successfully!", Toast.LENGTH_SHORT).show()
                    navigateToMain()
                } else {
                    Toast.makeText(this, "Sign up failed: ${task.exception?.message}", Toast.LENGTH_LONG).show()
                }
            }
    }

    private fun signInWithGoogle() {
        // Will implement Google Sign-In in next step
        Toast.makeText(this, "Google Sign-In coming soon!", Toast.LENGTH_SHORT).show()
    }

    private fun navigateToMain() {
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
        finish()
    }
}

@Composable
fun SignInScreen(
    onSignInClick: (String, String) -> Unit,
    onSwitchToSignUp: () -> Unit,
    onGoogleSignIn: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Welcome to TimerHaven Pro",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            singleLine = true
        )

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 24.dp),
            singleLine = true
        )

        Button(
            onClick = { onSignInClick(email, password) },
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
        ) {
            Text("Sign In")
        }

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedButton(
            onClick = onGoogleSignIn,
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
        ) {
            Text("Sign in with Google")
        }

        Spacer(modifier = Modifier.height(24.dp))

        TextButton(onClick = onSwitchToSignUp) {
            Text("Don't have an account? Sign Up")
        }
    }
}

@Composable
fun SignUpScreen(
    onSignUpClick: (String, String) -> Unit,
    onSwitchToSignIn: () -> Unit,
    onGoogleSignIn: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Create Your Account",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            singleLine = true
        )

        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password (min 6 characters)") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            singleLine = true
        )

        OutlinedTextField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = { Text("Confirm Password") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 24.dp),
            singleLine = true
        )

        Button(
            onClick = {
                if (password == confirmPassword) {
                    onSignUpClick(email, password)
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp),
            enabled = password.isNotBlank() && password == confirmPassword
        ) {
            Text("Create Account")
        }

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedButton(
            onClick = onGoogleSignIn,
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
        ) {
            Text("Sign up with Google")
        }

        Spacer(modifier = Modifier.height(24.dp))

        TextButton(onClick = onSwitchToSignIn) {
            Text("Already have an account? Sign In")
        }
    }
}
