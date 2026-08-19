import { View, Text, StyleSheet } from "react-native";
import { colors } from "../theme/colors";

export function MetricCard({
  label,
  value,
  unit,
  accent = colors.cyan,
}: {
  label: string;
  value: string | number;
  unit?: string;
  accent?: string;
}) {
  return (
    <View style={styles.card}>
      <View
        style={[
          styles.dot,
          {
            backgroundColor: accent,
          },
        ]}
      />

      <Text style={styles.label}>
        {label}
      </Text>

      <View style={styles.valueRow}>
        <Text style={styles.value}>
          {value}
        </Text>

        {unit ? (
          <Text style={styles.unit}>
            {unit}
          </Text>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flex: 1,
    minHeight: 104,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 16,
    padding: 14,
    margin: 4,
  },

  dot: {
    width: 7,
    height: 7,
    borderRadius: 4,
    marginBottom: 12,
  },

  label: {
    color: colors.muted,
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },

  valueRow: {
    flexDirection: "row",
    alignItems: "baseline",
    marginTop: 6,
  },

  value: {
    color: colors.text,
    fontSize: 25,
    fontWeight: "800",
  },

  unit: {
    color: colors.muted,
    fontSize: 11,
    marginLeft: 4,
  },
});