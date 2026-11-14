package com.sergenet.TimerHavenApp

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class SettingsActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            MaterialTheme {
                SettingsScreen(
                    onThemeSelected = { themeId ->
                        val success = ThemeManager.setTheme(this, themeId)
                        if (success) {
                            Toast.makeText(this, "Theme applied! Restart app to see changes.", Toast.LENGTH_LONG).show()
                            finish()
                        } else {
                            // Theme is locked, redirect to paywall
                            val intent = Intent(this, PaywallActivity::class.java)
                            startActivity(intent)
                        }
                    },
                    onBack = { finish() }
                )
            }
        }
    }
}

@Composable
fun SettingsScreen(
    onThemeSelected: (String) -> Unit,
    onBack: () -> Unit
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val themes = remember { ThemeManager.getAvailableThemes(context) }
    val currentTheme = remember { mutableStateOf(ThemeManager.getSelectedTheme(context)) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onBack) {
                Text("← Back")
            }
            Text(
                text = "Settings",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.width(60.dp))
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "Theme",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(16.dp))

        LazyColumn {
            items(themes) { theme ->
                ThemeItem(
                    theme = theme,
                    isSelected = theme.id == currentTheme.value,
                    onClick = {
                        currentTheme.value = theme.id
                        onThemeSelected(theme.id)
                    }
                )
                Spacer(modifier = Modifier.height(12.dp))
            }
        }
    }
}

@Composable
fun ThemeItem(
    theme: ThemeManager.ThemeOption,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) 
                MaterialTheme.colorScheme.primaryContainer 
            else 
                MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = theme.name,
                    fontSize = 18.sp,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                )
                
                if (theme.isLocked) {
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "PRO",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        modifier = Modifier
                            .background(
                                Color(0xFFFF6B00),
                                shape = RoundedCornerShape(4.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }
            
            if (isSelected) {
                Text("✓", fontSize = 20.sp, color = MaterialTheme.colorScheme.primary)
            }
        }
    }
}
