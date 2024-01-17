import { PixelRatio } from 'react-native';

export const dpToPx = (dp) => {
    PixelRatio.roundToNearestPixel(dp * (PixelRatio.get() / 160));
    return dp;
}