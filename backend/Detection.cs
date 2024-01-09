using Microsoft.EntityFrameworkCore;

namespace DoorbellBackend.Models
{
    public class Detection
    {
        // Auto generated Id
        public int Id { get; set; }
        public string? Name { get; set; }
        public string? Date { get; set; }
        public string? Address { get; set; }
        public string? Image { get; set; }
    }

    class DoorbellDb : DbContext
    {
        public DoorbellDb(DbContextOptions options) : base(options) { }
        public DbSet<Detection> Detections { get; set; } = null!;
    }
}