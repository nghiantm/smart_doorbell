import { PixelRatio } from 'react-native';
import { Dimensions } from 'react-native';

export const getScreenWidth = () => {
  return Dimensions.get('window').width;
};

export const dpToPx = (dp) => {
    PixelRatio.roundToNearestPixel(dp * (PixelRatio.get() / 160));
    return dp;
}