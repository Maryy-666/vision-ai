import { useState } from "react";

import {
  ActivityIndicator,
  Alert,
  Image,
  Pressable,
  ScrollView,
  Text,
  View,
} from "react-native";

import { useRouter } from "expo-router";

import * as ImagePicker from "expo-image-picker";

import { Ionicons } from "@expo/vector-icons";

import { SectionHeader } from "../components/SectionHeader";

import { colors } from "../theme/colors";
import { styles } from "../theme/styles";

import { uploadInspectionImage } from "../lib/api";

import { useInspection } from "../store/InspectionContext";

export default function ScanScreen() {
  const router = useRouter();

  const {
    imageUri,
    setImageUri,
    setImageResponse,
  } = useInspection();

  const [loading, setLoading] =
    useState(false);

  // ---------------------------------------------------------
  // Gallery
  // ---------------------------------------------------------

  async function pickFromGallery() {
    const permission =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permission.granted) {
      Alert.alert(
        "Permission required",
        "Photo library permission is required."
      );

      return;
    }

    const result =
      await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        allowsEditing: false,
        quality: 1,
      });

    if (!result.canceled) {
      const selectedImage =
        result.assets[0];

      setImageUri(
        selectedImage.uri
      );
    }
  }

  // ---------------------------------------------------------
  // Camera
  // ---------------------------------------------------------

  async function capturePhoto() {
    const permission =
      await ImagePicker.requestCameraPermissionsAsync();

    if (!permission.granted) {
      Alert.alert(
        "Permission required",
        "Camera permission is required."
      );

      return;
    }

    const result =
      await ImagePicker.launchCameraAsync({
        mediaTypes: ["images"],
        quality: 1,
      });

    if (!result.canceled) {
      const capturedImage =
        result.assets[0];

      setImageUri(
        capturedImage.uri
      );
    }
  }

  // ---------------------------------------------------------
  // Upload and analyze
  // ---------------------------------------------------------

  async function analyzeImage() {
    if (!imageUri) {
      return;
    }

    setLoading(true);

    try {
      const result =
        await uploadInspectionImage(
          imageUri,
          `inspection-${Date.now()}.jpg`
        );

      setImageResponse(result);

      router.push("/result");
    } catch (error: any) {
      Alert.alert(
        "Upload failed",
        error?.message ||
          "Could not analyze the image."
      );
    } finally {
      setLoading(false);
    }
  }

  // ---------------------------------------------------------
  // UI
  // ---------------------------------------------------------

  return (
    <View style={styles.screen}>
      <ScrollView
        contentContainerStyle={
          styles.content
        }
        showsVerticalScrollIndicator={false}
      >
        <SectionHeader
          eyebrow="STEP 02"
          title="Inspect an image"
        />

        {/* ------------------------------------------------ */}
        {/* Image preview */}
        {/* ------------------------------------------------ */}

        {imageUri ? (
          <View
            style={{
              borderRadius: 20,
              overflow: "hidden",
              backgroundColor:
                colors.surface,
              borderWidth: 1,
              borderColor:
                colors.border,
            }}
          >
            <Image
              source={{
                uri: imageUri,
              }}
              style={{
                width: "100%",
                height: 360,
              }}
              resizeMode="contain"
            />
          </View>
        ) : (
          <View
            style={[
              styles.card,
              {
                minHeight: 300,
                alignItems:
                  "center",
                justifyContent:
                  "center",
              },
            ]}
          >
            <View
              style={{
                width: 82,
                height: 82,
                borderRadius: 28,
                backgroundColor:
                  colors.cyanSoft,
                alignItems:
                  "center",
                justifyContent:
                  "center",
              }}
            >
              <Ionicons
                name="image-outline"
                size={38}
                color={colors.cyan}
              />
            </View>

            <Text
              style={[
                styles.cardTitle,
                {
                  marginTop: 18,
                },
              ]}
            >
              No image selected
            </Text>

            <Text
              style={[
                styles.cardText,
                {
                  textAlign:
                    "center",
                  maxWidth: 260,
                },
              ]}
            >
              Capture a sample part
              or choose an existing
              inspection image.
            </Text>
          </View>
        )}

        {/* ------------------------------------------------ */}
        {/* Camera / Gallery buttons */}
        {/* ------------------------------------------------ */}

        <View
          style={{
            flexDirection: "row",
            marginHorizontal: -5,
            marginTop: 14,
          }}
        >
          <Pressable
            onPress={
              capturePhoto
            }
            style={({ pressed }) => [
              styles.button,
              styles.buttonSecondary,
              {
                flex: 1,
                margin: 5,
                opacity: pressed
                  ? 0.8
                  : 1,
              },
            ]}
          >
            <Ionicons
              name="camera-outline"
              size={20}
              color={colors.text}
            />

            <Text
              style={[
                styles.buttonText,
                styles.secondaryText,
              ]}
            >
              Camera
            </Text>
          </Pressable>

          <Pressable
            onPress={
              pickFromGallery
            }
            style={({ pressed }) => [
              styles.button,
              styles.buttonSecondary,
              {
                flex: 1,
                margin: 5,
                opacity: pressed
                  ? 0.8
                  : 1,
              },
            ]}
          >
            <Ionicons
              name="images-outline"
              size={20}
              color={colors.text}
            />

            <Text
              style={[
                styles.buttonText,
                styles.secondaryText,
              ]}
            >
              Gallery
            </Text>
          </Pressable>
        </View>

        {/* ------------------------------------------------ */}
        {/* Analyze button */}
        {/* ------------------------------------------------ */}

        <Pressable
          disabled={
            !imageUri ||
            loading
          }
          onPress={
            analyzeImage
          }
          style={({ pressed }) => [
            styles.button,
            styles.buttonPrimary,
            {
              marginTop: 10,

              opacity:
                !imageUri ||
                loading
                  ? 0.45
                  : pressed
                    ? 0.8
                    : 1,
            },
          ]}
        >
          {loading ? (
            <ActivityIndicator
              color={colors.black}
            />
          ) : (
            <>
              <Ionicons
                name="scan-outline"
                size={21}
                color={colors.black}
              />

              <Text
                style={[
                  styles.buttonText,
                  styles.primaryText,
                ]}
              >
                Run Vision Analysis
              </Text>
            </>
          )}
        </Pressable>

        {/* ------------------------------------------------ */}
        {/* Pipeline information */}
        {/* ------------------------------------------------ */}

        <View
          style={[
            styles.card,
            {
              marginTop: 18,
            },
          ]}
        >
          <Text
            style={styles.cardTitle}
          >
            Current pipeline
          </Text>

          <Text
            style={styles.cardText}
          >
            Upload → grayscale → blur →
            Canny → morphology →
            connected components →
            candidate regions
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}