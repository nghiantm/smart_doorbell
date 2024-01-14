namespace DoorbellBackend.ImageHelper;
public class ImageHelper
{
    public static string SaveImageLocally(string base64Image, string name, string date)
    {
        {
            byte[] imageData = Convert.FromBase64String(base64Image);
            string imagePath = StoreImage(imageData, name, date);

            // Return the relative path
            return imagePath;
        }
    }

    private static string StoreImage(byte[] imageData, string name, string date)
    {
        string directoryPath = $"assets/images/{name}/";
        if (!Directory.Exists(directoryPath))
        {
            Directory.CreateDirectory(directoryPath);
        }

        string fileName = $"{date}_{name}.jpg";
        string filePath = Path.Combine(directoryPath, fileName);

        File.WriteAllBytes(filePath, imageData);

        // Return the relative path
        return filePath;
    }

    public static string ConvertToBase64(string imagePath)
    {
        byte[] imageData = File.ReadAllBytes(imagePath);
        return Convert.ToBase64String(imageData);
    }
};