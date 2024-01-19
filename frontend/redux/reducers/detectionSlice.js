import { createSlice } from "@reduxjs/toolkit";

export const detectionSlice = createSlice({
    name: 'detection',
    initialState: {
        address: '',
        detections: []
    },
    reducers: {
        setAddress: (state, action) => {
            state.address.push(action.payload);
        },
        addDetections: (state, action) => {
            state.detections.push(...action.payload);
        }
    }
})

export const { setAddress, addDetections } = detectionSlice.actions;

export default detectionSlice.reducer;