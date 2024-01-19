import { createStackNavigator } from "@react-navigation/stack";
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import React from "react";
import { SafeAreaView, StyleSheet, Text, View } from "react-native";
import Home from "./screens/Home";
import Setting from "./screens/Setting";
import Initial from "./screens/Initial";

const Stack = createNativeStackNavigator();

const AppNavigator = () => {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Welcome" component={Initial} />
            <Stack.Screen name="Home" component={Home} />
            <Stack.Screen name="Setting" component={Setting} />
        </Stack.Navigator>
    );
};

const styles = StyleSheet.create({
    text: {
        color: "#000",
    },
    bg: {
        backgroundColor: "#000"
    }
});

export default AppNavigator;