import { useState } from "react";
import { useRouter } from "expo-router";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { SectionHeader } from "../components/SectionHeader";
import { StatusPill } from "../components/StatusPill";
import { colors } from "../theme/colors";
import { styles } from "../theme/styles";
import { sendAgentMessage } from "../lib/api";
import { useInspection } from "../store/InspectionContext";

const exampleRequirement =
  "Inspect a steel metal component for scratches. " +
  "Reflective steel surface. " +
  "Minimum defect 0.2 mm. " +
  "FOV 200 mm. " +
  "Object length 100 mm. " +
  "Working distance 300 mm. " +
  "Conveyor speed 0.5 m/s.";

export default function InspectScreen() {
  const router = useRouter();

  const {
    sessionId,
    setSessionId,
    requirement,
    setRequirement,
    agentResponse,
    setAgentResponse,
  } = useInspection();

  const [message, setMessage] =
    useState(requirement);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const currentQuestion =
    agentResponse?.missing_information?.[0]?.question;

  async function submitMessage() {
    const text = message.trim();

    if (!text) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result =
        await sendAgentMessage(
          text,
          sessionId
        );

      setRequirement(text);

      setAgentResponse(result);

      if (result.session_id) {
        setSessionId(result.session_id);
      }

      /*
       * Gereksinim tamamlandıysa
       * image inspection ekranına geç.
       */
      if (result.status === "success") {
        router.push("/scan");
        return;
      }

      /*
       * Backend eksik bilgi istediyse
       * input'u temizle ve kullanıcıdan
       * yeni cevabı bekle.
       */
      if (
        result.status ===
        "needs_information"
      ) {
        setMessage("");
      }
    } catch (err: any) {
      setError(
        err?.message ||
          "Could not reach the Vision Agent backend."
      );
    } finally {
      setLoading(false);
    }
  }

  function useExample() {
    setMessage(exampleRequirement);
  }

  return (
    <View style={styles.screen}>
      <ScrollView
        contentContainerStyle={
          styles.content
        }
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        <SectionHeader
          eyebrow="STEP 01"
          title="Define inspection"
        />

        {/* Session status */}
        <View
          style={[
            styles.card,
            {
              marginBottom: 16,
            },
          ]}
        >
          <StatusPill
            label={
              sessionId
                ? "SESSION ACTIVE"
                : "NEW SESSION"
            }
            tone="cyan"
          />

          <Text
            style={[
              styles.cardText,
              {
                marginTop: 12,
              },
            ]}
          >
            Describe the part, defect,
            surface, minimum defect size
            and known camera geometry.
          </Text>
        </View>

        {/* Agent question */}
        {currentQuestion ? (
          <View
            style={[
              styles.card,
              {
                marginBottom: 16,
                borderColor:
                  colors.amber,
              },
            ]}
          >
            <Text
              style={[
                styles.label,
                {
                  color:
                    colors.amber,
                },
              ]}
            >
              AGENT QUESTION
            </Text>

            <Text
              style={{
                color: colors.text,
                fontSize: 17,
                lineHeight: 24,
                fontWeight: "700",
              }}
            >
              {currentQuestion}
            </Text>
          </View>
        ) : null}

        {/* Input label */}
        <Text style={styles.label}>
          {currentQuestion
            ? "YOUR ANSWER"
            : "INSPECTION REQUIREMENT"}
        </Text>

        {/* Main input */}
        <TextInput
          value={message}
          onChangeText={setMessage}
          placeholder={
            currentQuestion
              ? "e.g. 4"
              : "Describe your inspection..."
          }
          placeholderTextColor={
            colors.muted
          }
          multiline
          textAlignVertical="top"
          style={[
            styles.input,
            {
              minHeight:
                currentQuestion
                  ? 70
                  : 150,
              paddingTop: 14,
            },
          ]}
        />

        {/* Example button */}
        {!currentQuestion ? (
          <Pressable
            onPress={useExample}
            style={({ pressed }) => [
              styles.button,
              styles.buttonSecondary,
              {
                marginTop: 10,
                opacity: pressed
                  ? 0.8
                  : 1,
              },
            ]}
          >
            <Ionicons
              name="sparkles-outline"
              size={18}
              color={colors.cyan}
            />

            <Text
              style={[
                styles.buttonText,
                styles.secondaryText,
              ]}
            >
              Use Example
            </Text>
          </Pressable>
        ) : null}

        {/* Error */}
        {error ? (
          <View
            style={[
              styles.card,
              {
                marginTop: 14,
                borderColor:
                  colors.red,
              },
            ]}
          >
            <Text
              style={{
                color: colors.red,
                fontSize: 13,
                lineHeight: 19,
              }}
            >
              {error}
            </Text>
          </View>
        ) : null}

        {/* Submit */}
        <Pressable
          disabled={
            loading ||
            !message.trim()
          }
          onPress={
            submitMessage
          }
          style={({ pressed }) => [
            styles.button,
            styles.buttonPrimary,
            {
              marginTop: 16,
              opacity:
                loading ||
                !message.trim()
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
              <Text
                style={[
                  styles.buttonText,
                  styles.primaryText,
                ]}
              >
                {currentQuestion
                  ? "Send Answer"
                  : "Analyze Requirement"}
              </Text>

              <Ionicons
                name="arrow-forward"
                size={20}
                color={colors.black}
              />
            </>
          )}
        </Pressable>

        {/* Success preview */}
        {agentResponse?.status ===
          "success" && (
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
              Engineering design ready
            </Text>

            <Text
              style={styles.cardText}
            >
              Camera, lens, lighting
              and vision strategy have
              been calculated. Continue
              to image inspection.
            </Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}