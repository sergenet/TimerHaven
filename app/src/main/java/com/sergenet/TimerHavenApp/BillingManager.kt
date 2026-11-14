package com.sergenet.TimerHavenApp

import android.app.Activity
import android.util.Log
import com.android.billingclient.api.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class BillingManager(
    private val activity: Activity,
    private val onPurchaseSuccess: () -> Unit,
    private val onPurchaseFailure: (String) -> Unit
) {
    private lateinit var billingClient: BillingClient
    private val coroutineScope = CoroutineScope(Dispatchers.Main)
    
    companion object {
        const val PRODUCT_ID_MONTHLY = "timerhaven_pro_monthly"
        const val PRODUCT_ID_ANNUAL = "timerhaven_pro_annual"
        private const val TAG = "BillingManager"
    }

    private val purchasesUpdatedListener = PurchasesUpdatedListener { billingResult, purchases ->
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (purchase in purchases) {
                handlePurchase(purchase)
            }
        } else if (billingResult.responseCode == BillingClient.BillingResponseCode.USER_CANCELED) {
            Log.d(TAG, "User canceled purchase")
            onPurchaseFailure("Purchase canceled")
        } else {
            Log.e(TAG, "Purchase failed: ${billingResult.debugMessage}")
            onPurchaseFailure("Purchase failed: ${billingResult.debugMessage}")
        }
    }

    fun initialize() {
        billingClient = BillingClient.newBuilder(activity)
            .setListener(purchasesUpdatedListener)
            .enablePendingPurchases(
                PendingPurchasesParams.newBuilder()
                    .enableOneTimeProducts()
                    .build()
            )
            .build()

        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(billingResult: BillingResult) {
                if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                    Log.d(TAG, "Billing client connected")
                    // Query active subscriptions
                    queryActivePurchases()
                } else {
                    Log.e(TAG, "Billing setup failed: ${billingResult.debugMessage}")
                }
            }

            override fun onBillingServiceDisconnected() {
                Log.w(TAG, "Billing service disconnected")
            }
        })
    }

    fun purchaseMonthly() {
        purchaseSubscription(PRODUCT_ID_MONTHLY)
    }

    fun purchaseAnnual() {
        purchaseSubscription(PRODUCT_ID_ANNUAL)
    }

    private fun purchaseSubscription(productId: String) {
        coroutineScope.launch {
            val productDetailsResult = withContext(Dispatchers.IO) {
                billingClient.queryProductDetails(
                    QueryProductDetailsParams.newBuilder()
                        .setProductList(
                            listOf(
                                QueryProductDetailsParams.Product.newBuilder()
                                    .setProductId(productId)
                                    .setProductType(BillingClient.ProductType.SUBS)
                                    .build()
                            )
                        )
                        .build()
                )
            }

            if (productDetailsResult.billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                val productDetails = productDetailsResult.productDetailsList?.firstOrNull()
                if (productDetails != null) {
                    launchPurchaseFlow(productDetails)
                } else {
                    onPurchaseFailure("Product not found")
                }
            } else {
                onPurchaseFailure("Failed to load product details")
            }
        }
    }

    private fun launchPurchaseFlow(productDetails: ProductDetails) {
        val offerToken = productDetails.subscriptionOfferDetails?.firstOrNull()?.offerToken
        if (offerToken == null) {
            onPurchaseFailure("No subscription offer available")
            return
        }

        val productDetailsParamsList = listOf(
            BillingFlowParams.ProductDetailsParams.newBuilder()
                .setProductDetails(productDetails)
                .setOfferToken(offerToken)
                .build()
        )

        val billingFlowParams = BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(productDetailsParamsList)
            .build()

        billingClient.launchBillingFlow(activity, billingFlowParams)
    }

    private fun handlePurchase(purchase: Purchase) {
        if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
            if (!purchase.isAcknowledged) {
                acknowledgePurchase(purchase)
            } else {
                onPurchaseSuccess()
            }
        }
    }

    private fun acknowledgePurchase(purchase: Purchase) {
        val acknowledgePurchaseParams = AcknowledgePurchaseParams.newBuilder()
            .setPurchaseToken(purchase.purchaseToken)
            .build()

        coroutineScope.launch {
            val result = withContext(Dispatchers.IO) {
                billingClient.acknowledgePurchase(acknowledgePurchaseParams)
            }
            
            if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                Log.d(TAG, "Purchase acknowledged")
                onPurchaseSuccess()
            } else {
                Log.e(TAG, "Failed to acknowledge purchase: ${result.debugMessage}")
                onPurchaseFailure("Failed to complete purchase")
            }
        }
    }

    fun queryActivePurchases() {
        coroutineScope.launch {
            val purchasesResult = withContext(Dispatchers.IO) {
                billingClient.queryPurchasesAsync(
                    QueryPurchasesParams.newBuilder()
                        .setProductType(BillingClient.ProductType.SUBS)
                        .build()
                )
            }

            if (purchasesResult.billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                val activePurchases = purchasesResult.purchasesList
                Log.d(TAG, "Active subscriptions: ${activePurchases.size}")
                
                // Save subscription status
                val hasPro = activePurchases.any { purchase ->
                    purchase.products.contains(PRODUCT_ID_MONTHLY) ||
                    purchase.products.contains(PRODUCT_ID_ANNUAL)
                }
                
                SubscriptionManager.updateSubscriptionStatus(activity, hasPro)
            }
        }
    }

    fun endConnection() {
        billingClient.endConnection()
    }
}
