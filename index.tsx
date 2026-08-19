import { useRouter } from "expo-router";
import {
  Pressable,
  ScrollView,
  Text,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { StatusPill } from "../components/StatusPill";
import { colors } from "../theme/colors";
import { styles } from "../theme/styles";
import { useInspection } from "../store/InspectionContext";
import { MetricCard } from "../theme/MetricCard";

export default function HomeScreen() {
  const router = useRouter();

  const { reset } = useInspection();

  function startInspection() {
    reset();

    router.push("/inspect");
  }

  return (
    <View style={styles.screen}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View
          style={{
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <View>
            <Text style={styles.eyebrow}>
              VISION AGENT
            </Text>

            <Text style={styles.title}>
              Inspection{"\n"}
              Control Center
            </Text>
          </View>

          <View
            style={{
              width: 46,
              height: 46,
              borderRadius: 15,
              backgroundColor: colors.cyanSoft,
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Ionicons
              name="scan-outline"
              size={24}
              color={colors.cyan}
            />
          </View>
        </View>

        {/* Description */}
        <Text style={styles.subtitle}>
          AI-assisted machine vision engineering
          and image inspection.
        </Text>

        {/* Backend status */}
        <View style={{ marginTop: 22 }}>
          <StatusPill
            label="BACKEND READY"
            tone="green"
          />
        </View>

        {/* Start inspection */}
        <Pressable
          onPress={startInspection}
          style={({ pressed }) => [
            styles.button,
            styles.buttonPrimary,
            {
              marginTop: 18,
              opacity: pressed ? 0.8 : 1,
            },
          ]}
        >
          <Ionicons
            name="add-circle-outline"
            size={22}
            color={colors.black}
          />

          <Text
            style={[
              styles.buttonText,
              styles.primaryText,
            ]}
          >
            Start New Inspection
          </Text>
        </Pressable>

        {/* Metrics row 1 */}
        <View
          style={{
            flexDirection: "row",
            marginHorizontal: -4,
            marginTop: 18,
          }}
        >
          <MetricCard
            label="Architecture"
            value="Area"
            unit="Scan"
          />

          <MetricCard
            label="Min defect"
            value="0.2"
            unit="mm"
            accent={colors.amber}
          />
        </View>

        {/* Metrics row 2 */}
        <View
          style={{
            flexDirection: "row",
            marginHorizontal: -4,
          }}
        >
          <MetricCard
            label="Resolution"
            value="4000"
            unit="px"
            accent={colors.green}
          />

          <MetricCard
            label="FPS"
            value="6"
            unit="fps"
          />
        </View>

        {/* How it works */}
        <View
          style={[
            styles.card,
            {
              marginTop: 14,
            },
          ]}
        >
          <Text style={styles.cardTitle}>
            How it works
          </Text>

          <Text style={styles.cardText}>
            01  Describe the inspection requirement{"\n"}
            02  Complete missing engineering parameters{"\n"}
            03  Upload or capture a sample image{"\n"}
            04  Review engineering and vision candidates
          </Text>
        </View>

        {/* MVP note */}
        <Text
          style={{
            color: colors.muted,
            fontSize: 11,
            lineHeight: 17,
            marginTop: 20,
          }}
        >
          MVP note: image candidates are
          edge/morphology regions. Physical
          mm calibration and production
          PASS/FAIL validation are not yet
          implemented.
        </Text>
      </ScrollView>
    </View>
  );
}