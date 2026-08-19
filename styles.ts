import { StyleSheet } from "react-native";
import { colors } from "./colors";

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
  },

  content: {
    paddingHorizontal: 20,
    paddingTop: 18,
    paddingBottom: 36,
  },

  eyebrow: {
    color: colors.cyan,
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 1.8,
    textTransform: "uppercase",
  },

  title: {
    color: colors.text,
    fontSize: 30,
    lineHeight: 36,
    fontWeight: "800",
    marginTop: 7,
  },

  subtitle: {
    color: colors.muted,
    fontSize: 14,
    lineHeight: 21,
    marginTop: 8,
  },

  card: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 18,
    padding: 16,
  },

  cardTitle: {
    color: colors.text,
    fontSize: 16,
    fontWeight: "800",
  },

  cardText: {
    color: colors.muted,
    fontSize: 13,
    lineHeight: 19,
    marginTop: 5,
  },

  button: {
    minHeight: 52,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 18,
    flexDirection: "row",
    gap: 8,
  },

  buttonPrimary: {
    backgroundColor: colors.cyan,
  },

  buttonSecondary: {
    backgroundColor: colors.surface2,
    borderWidth: 1,
    borderColor: colors.border,
  },

  buttonText: {
    fontSize: 15,
    fontWeight: "800",
  },

  primaryText: {
    color: colors.black,
  },

  secondaryText: {
    color: colors.text,
  },

  input: {
    minHeight: 52,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
    color: colors.text,
    paddingHorizontal: 15,
    fontSize: 15,
  },

  label: {
    color: colors.muted,
    fontSize: 12,
    fontWeight: "700",
    marginBottom: 8,
  },

  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  divider: {
    height: 1,
    backgroundColor: colors.border,
    marginVertical: 16,
  },
});