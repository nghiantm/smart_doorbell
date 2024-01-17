import { configureStore } from "@reduxjs/toolkit";
import detectionSlice from "./reducers/detectionSlice";

export default configureStore({
    reducer: {
        detection: detectionSlice
    },
})