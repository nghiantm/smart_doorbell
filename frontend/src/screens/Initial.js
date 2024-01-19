import { useState } from "react";
import { StyleSheet, Text, View, TextInput, Button } from "react-native"
import { dpToPx } from "../utils/helpers";
import {widthPercentageToDP as wp, heightPercentageToDP as hp} from 'react-native-responsive-screen';
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import { addDetections } from "../../redux/reducers/detectionSlice";

const Initial = ({ navigation }) => {
    const [address, setAdress] = useState('');
    console.log(address)
    const [error, setError] = useState('');
    const dispatch = useDispatch();

    const handleButtonPress = (ip) => {
        console.log(ip);
        axios
            .get(`http://${ip}/detections?page=1&pageSize=10`)
            .then((res) => {
                dispatch(addDetections(res.data));
                navigation.replace('Home');
            })
            .catch((err) => {
                setError(err.text)
            })
    }

    return (
        <View style={styles.container}>
            <Text style={styles.text}>What's the host address?</Text>
            <TextInput 
                value={address}
                onChangeText={text => setAdress(text)}
                style={styles.input}
                placeholder='e.g 192.168.0.1:xxxx'
                placeholderTextColor='#aaa'
            />
            <Button 
                onPress={() => handleButtonPress(address)}
                title="Enter"
                style={styles.button}
            />
            {
                error ? <Text>{error}</Text> : null
            }
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        width: wp('80%'),
        alignSelf: 'center'
    },
    text: {
        fontSize: hp('2%'),
        backgroundColor: '#f2f2f2',
        alignSelf: 'center'
    },
    input: {
        height: hp('5%'),
        alignItems: 'center',
        textAlign: 'center',
        backgroundColor: '',
        borderColor: '#000',
        borderWidth: 1,
        borderRadius: dpToPx(8)
    },
    button: {
    }
})

export default Initial;