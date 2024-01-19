import { dpToPx, getScreenWidth } from "../utils/helpers"

export const mediumFont = () => {
    const width = getScreenWidth();

    // Define breakpoints and corresponding margins
    const breakpoints = {
        small: 600,
        medium: 900,
        large: 1200,
    };

    // Determine the font size based on screen width
    if (width < breakpoints.small) {
        return dpToPx(16);
    } else if (width > breakpoints.large) {
        return dpToPx(32);
    } else {
        return dpToPx(24);
    }
}