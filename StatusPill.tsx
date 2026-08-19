import { Text, View, StyleSheet } from "react-native";
import { colors } from "../theme/colors";

type StatusTone = "cyan" | "green" | "amber" | "red";

interface StatusPillProps {
  label: string;
  tone?: StatusTone;
}

export function StatusPill({
  label,
  tone = "cyan",
}: StatusPillProps) {
  const toneColors = {
    cyan: {
      background: colors.cyanSoft,
      foreground: colors.cyan,
    },

    green: {
      background: colors.greenSoft,
      foreground: colors.green,
    },

    amber: {
      background: colors.amberSoft,
      foreground: colors.amber,
    },

    red: {
      background: colors.redSoft,
      foreground: colors.red,
    },
  };

  const selected = toneColors[tone];

  return (
    <View
      style={[
        styles.pill,
        {
          backgroundColor: selected.background,
        },
      ]}
    >
      <View
        style={[
          styles.dot,
          {
            backgroundColor: selected.foreground,
          },
        ]}
      />

      <Text
        style={[
          styles.text,
          {
            color: selected.foreground,
          },
        ]}
      >
        {label}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  pill: {
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "flex-start",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    gap: 6,
  },

  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },

  text: {
    fontSize: 11,
    fontWeight: "800",
  },
});