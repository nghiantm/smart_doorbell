using Microsoft.OpenApi.Models;
using Microsoft.EntityFrameworkCore;
using DoorbellBackend.Models;
using DoorbellBackend.ImageHelper;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("Detections") ?? "Data Source=Detections.db";

// set up Swagger documentation
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSqlite<DoorbellDb>(connectionString);
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Doorbell API",
        Description = "Backend for camera script and frontend",
        Version = "v1"
    });
});

var app = builder.Build();

// set up Swagger documentation
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Doorbell API V1");
});

// APIs
app.MapGet("/detections", async (DoorbellDb db, int page, int pageSize = 10) =>
{
    var offset = (page - 1) * pageSize;

    var detections = await db.Detections
        .OrderByDescending(d => d.Id)
        .Skip(offset)
        .Take(pageSize)
        .ToListAsync();

    // convert local path to base64
    foreach (var detection in detections)
    {
        detection.Image = ImageHelper.ConvertToBase64(detection.Image);
    }

    return Results.Ok(detections);
});

app.MapGet("/detection/{id}", async (DoorbellDb db, int id) => await db.Detections.FindAsync(id));

app.MapPost("/detection", async (DoorbellDb db, Detection detection) =>
{
    if (detection.Image is null) return Results.BadRequest("No image found.");

    // convert base64 string to image and store locally, storing relative path in db
    detection.Image = ImageHelper.SaveImageLocally(detection.Image, detection.Name, detection.Date);

    await db.Detections.AddAsync(detection);
    await db.SaveChangesAsync();
    return Results.Created($"/detection/{detection.Date}_{detection.Name}.jpg", detection);
});
app.MapPut("/detection/{id}", async (DoorbellDb db, Detection updateDetection, int id) =>
{
    var detection = await db.Detections.FindAsync(id);
    if (detection is null) return Results.NotFound();
    detection.Name = updateDetection.Name;
    detection.Date = updateDetection.Date;
    detection.Address = updateDetection.Address;
    detection.Image = updateDetection.Image;
    await db.SaveChangesAsync();
    return Results.NoContent();
});

app.MapDelete("/detection/{id}", async (DoorbellDb db, int id) =>
{
    var detection = await db.Detections.FindAsync(id);
    if (detection is null) return Results.NotFound();
    db.Detections.Remove(detection);
    await db.SaveChangesAsync();
    return Results.Ok();
});

app.Run();
