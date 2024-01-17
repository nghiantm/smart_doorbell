import { FlashList } from "@shopify/flash-list";
import axios from "axios";
import React, { useEffect } from "react";
import { FlatList, Image, StyleSheet, Text, View } from "react-native";
import { useDispatch, useSelector } from "react-redux";
import { addDetections } from "../../redux/reducers/detectionSlice";
import { dpToPx } from "../utils/helpers";

const Home = () => {
    const detections = useSelector((state) => state.detection.detections);
    const dispatch = useDispatch();

    useEffect(() => {
        axios
            .get('http://localhost:5214/detections?page=1&pageSize=10')
            .then((res) => {
                dispatch(addDetections(res.data))
            })
    }, [])

    return (
        <View style={styles.flashView}>
            <FlatList 
                data={detections}
                renderItem={({ item }) => renderItem(item)}
                estimatedItemSize={100}
            />
        </View>
    );
};

const renderItem = (item) => {
    return (
        <View style={styles.renderItem}>
            <Image 
                style={{ width: '50%', aspectRatio: 1920/1080}}
                source={{
                    uri: `data:image/jpg;base64,${item.image}`
                }}
            />
            <Text style={styles.text}>{item.name}</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    renderItem: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: '#000',
        height: '100%'
    },
    text: {
        color: "#fff"
    },
})

export default Home;