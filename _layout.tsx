import { Stack } from "expo-router";

import { InspectionProvider } from "../store/InspectionContext";
import { colors } from "../theme/colors";
import { StatusBar } from "react-native";

export default function RootLayout() {
  return (
    <InspectionProvider>
      <StatusBar barStyle="light-content" />

      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: colors.bg,
          },

          headerTintColor: colors.text,

          headerShadowVisible: false,

          contentStyle: {
            backgroundColor: colors.bg,
          },

          headerTitleStyle: {
            fontWeight: "800",
          },
        }}
      >
        <Stack.Screen
          name="index"
          options={{
            headerShown: false,
          }}
        />

        <Stack.Screen
          name="inspect"
          options={{
            title: "New Inspection",
          }}
        />

        <Stack.Screen
          name="scan"
          options={{
            title: "Image Inspection",
          }}
        />

        <Stack.Screen
          name="result"
          options={{
            title: "Inspection Result",
          }}
        />
      </Stack>
    </InspectionProvider>
  );
}