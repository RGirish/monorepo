plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.girish.signalchat"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.girish.signalchat"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation(platform("androidx.compose:compose-bom:2024.10.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")

    // Provides the XML Theme.Material3.* styles the manifest references -- the
    // androidx.compose.material3 dependency above is Compose-only Kotlin and
    // ships no XML style resources, so AAPT can't resolve the manifest theme
    // without this one too.
    implementation("com.google.android.material:material:1.14.0")

    // Signal's own implementation of X3DH + the Double Ratchet.
    implementation("org.signal:libsignal-android:0.76.1")

    // libsignal-android needs Java 8+ APIs desugared for older minSdk levels.
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.0.3")
}
