import { View, Text, StyleSheet } from "react-native";
import { colors } from "../theme/colors";
interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
}

export function SectionHeader({
  eyebrow,
  title,
}: SectionHeaderProps) {
  return (
    <View style={styles.container}>
      {eyebrow ? (
        <Text style={styles.eyebrow}>
          {eyebrow}
        </Text>
      ) : null}

      <Text style={styles.title}>
        {title}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 14,
  },

  eyebrow: {
    color: colors.cyan,
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 1.4,
    textTransform: "uppercase",
    marginBottom: 5,
  },

  title: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "800",
  },
});