package com.sergenet.timerhaven.ui

import androidx.core.net.toUri
import android.content.Intent
import android.util.Log
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.shape.RoundedCornerShape
import java.util.Locale
import com.sergenet.timerhaven.WebViewActivity
import kotlin.math.abs

private const val LOG_TAG = "TimerHaven"

private val tools = listOf(
    "Calendar",
    "Clipboard Manager",
    "Countdown Timer",
    "Currency Converter",
    "Focus Music",
    "Habit Tracker",
    "Meeting Planner",
    "Notes",
    "Password Generator",
    "Pomodoro Timer",
    "Stopwatch",
    "Task Timer",
    "Unit Converter",
    "Weather",
    "World Clock"
)

private val toolToSlug = mapOf(
    "Calendar" to "calendar",
    "Clipboard Manager" to "clipboard-manager",
    "Countdown Timer" to "countdown",
    "Currency Converter" to "currency",
    "Focus Music" to "focus-music",
    "Habit Tracker" to "habit-tracker",
    "Meeting Planner" to "meeting-planner",
    "Notes" to "notes",
    "Password Generator" to "password-generator",
    "Pomodoro Timer" to "pomodoro",
    "Stopwatch" to "stopwatch",
    "Task Timer" to "timer",
    "Unit Converter" to "unit-converter",
    "Weather" to "weather",
    "World Clock" to "world-clock"
)

@Composable
fun ToolsApp() {
    val selectedLangState = remember { mutableStateOf("en") }
    ToolsScreen(tools = tools, selectedLang = selectedLangState.value)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ToolsScreen(tools: List<String>, selectedLang: String) {
    val context = LocalContext.current

    Scaffold(
        topBar = { TopAppBar(title = { Text("TimerHaven Tools") }) }
    ) { innerPadding ->
        ToolsGrid(
            tools = tools,
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
        ) { tool ->
            val slug = toolToSlug[tool] ?: tool.lowercase(Locale.getDefault())
                .replace("[^a-z0-9]+".toRegex(), "-")
            val url = "https://timerhaven.com/${slug}-${selectedLang}.html"

            Log.d(LOG_TAG, "Tool tapped: $tool -> $url")

            try {
                val intent = Intent(context, WebViewActivity::class.java).apply {
                    putExtra("url", url)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                context.startActivity(intent)
            } catch (e: Exception) {
                Log.e(LOG_TAG, "Failed to open tool in-app: ${e.message}", e)
                try {
                    val fallback = Intent(Intent.ACTION_VIEW, url.toUri())
                    fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    context.startActivity(fallback)
                } catch (_: Exception) { /* ignore */ }
            }
        }
    }
}

/**
 * Adaptive neutral palette grid with tighter vertical spacing
 * - GridCells.Adaptive(minSize = 120.dp) adapts columns to screen width
 * - Softer neutral/beige-gray palette
 * - Reduced paddings and card height so more rows are visible on the same page
 */
@Composable
fun ToolsGrid(
    tools: List<String>,
    modifier: Modifier = Modifier,
    onItemClick: (String) -> Unit
) {
    // Softer neutral/beige-gray palette
    val neutralColors = listOf(
        Color(0xFFF7F5F2), // very light warm
        Color(0xFFF0ECE6),
        Color(0xFFE7E1D9),
        Color(0xFFDCD6CD),
        Color(0xFFD0C9BF),
        Color(0xFFC4BFB5)  // a touch darker for contrast variety
    )

    LazyVerticalGrid(
        // adaptive columns; cells will be at least 120.dp wide
        columns = GridCells.Adaptive(minSize = 120.dp),
        // tightened content padding and spacing
        contentPadding = PaddingValues(8.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = modifier
    ) {
        items(tools) { tool ->
            val bg = neutralColors[abs(tool.hashCode()) % neutralColors.size]

            // Simple luminance-like check to pick readable text color
            val luminanceApprox = bg.red * 0.2126f + bg.green * 0.7152f + bg.blue * 0.0722f
            val textColor = if (luminanceApprox > 0.65f) Color(0xFF0B2545) else Color.White

            Card(
                modifier = Modifier
                    // reduced height to just fit two lines comfortably
                    .height(96.dp)
                    .clickable { onItemClick(tool) },
                colors = CardDefaults.cardColors(containerColor = bg),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Box(
                    modifier = Modifier
                        .padding(8.dp)
                        .fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tool,
                        color = textColor,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        textAlign = TextAlign.Center,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}