import { createSlice } from "@reduxjs/toolkit";

export const detectionSlice = createSlice({
    name: 'detection',
    initialState: {
        detections: []
    },
    reducers: {
        addDetections: (state, action) => {
            state.detections.push(...action.payload);
        }
    }
})

export const { addDetections } = detectionSlice.actions;

export default detectionSlice.reducer;