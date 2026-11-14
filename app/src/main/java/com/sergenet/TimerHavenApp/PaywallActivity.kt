package com.sergenet.TimerHavenApp

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class PaywallActivity : ComponentActivity() {
    private lateinit var billingManager: BillingManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        billingManager = BillingManager(
            activity = this,
            onPurchaseSuccess = {
                Toast.makeText(this, "Welcome to TimerHaven Pro!", Toast.LENGTH_LONG).show()
                finish()
            },
            onPurchaseFailure = { error ->
                Toast.makeText(this, error, Toast.LENGTH_LONG).show()
            }
        )
        billingManager.initialize()

        setContent {
            MaterialTheme {
                PaywallScreen(
                    onMonthlyClick = { billingManager.purchaseMonthly() },
                    onAnnualClick = { billingManager.purchaseAnnual() },
                    onClose = { finish() }
                )
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        billingManager.endConnection()
    }
}

@Composable
fun PaywallScreen(
    onMonthlyClick: () -> Unit,
    onAnnualClick: () -> Unit,
    onClose: () -> Unit
) {
    var selectedPlan by remember { mutableStateOf("annual") } // Default to annual (better value)

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Close button at top-right
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.End
            ) {
                IconButton(onClick = onClose) {
                    Text("✕", fontSize = 24.sp, color = MaterialTheme.colorScheme.onSurface)
                }
            }
            
            // Header
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "Upgrade to Pro",
                style = MaterialTheme.typography.headlineLarge,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "Unlock all premium features",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(32.dp))

            // Features List
            FeatureItem("☁️ Cloud Sync - Access data on all devices")
            FeatureItem("🚫 Ad-Free Experience")
            FeatureItem("🎨 Premium Themes")
            FeatureItem("📊 Advanced Analytics Dashboard")
            FeatureItem("🔄 Unlimited Clipboard History")
            FeatureItem("💾 Priority Cloud Backup")

            Spacer(modifier = Modifier.height(32.dp))

            // Pricing Cards
            PricingCard(
                title = "Annual",
                price = "$24.99",
                period = "per year",
                savings = "Save 30%!",
                isSelected = selectedPlan == "annual",
                onClick = { selectedPlan = "annual" }
            )

            Spacer(modifier = Modifier.height(16.dp))

            PricingCard(
                title = "Monthly",
                price = "$2.99",
                period = "per month",
                savings = null,
                isSelected = selectedPlan == "monthly",
                onClick = { selectedPlan = "monthly" }
            )

            Spacer(modifier = Modifier.weight(1f))

            // Purchase Button
            Button(
                onClick = {
                    if (selectedPlan == "annual") {
                        onAnnualClick()
                    } else {
                        onMonthlyClick()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary
                )
            ) {
                Text(
                    text = "Subscribe Now",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            TextButton(onClick = onClose) {
                Text("Maybe Later")
            }

            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
fun FeatureItem(text: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.bodyLarge
        )
    }
}

@Composable
fun PricingCard(
    title: String,
    price: String,
    period: String,
    savings: String?,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(
                width = if (isSelected) 3.dp else 1.dp,
                color = if (isSelected) MaterialTheme.colorScheme.primary else Color.Gray,
                shape = RoundedCornerShape(12.dp)
            ),
        onClick = onClick,
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
                .padding(20.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = title,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = period,
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = price,
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                if (savings != null) {
                    Text(
                        text = savings,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF4CAF50),
                        modifier = Modifier
                            .background(
                                Color(0xFF4CAF50).copy(alpha = 0.1f),
                                shape = RoundedCornerShape(4.dp)
                            )
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }
        }
    }
}
