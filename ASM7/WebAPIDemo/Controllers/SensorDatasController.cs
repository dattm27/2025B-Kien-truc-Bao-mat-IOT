using Microsoft.AspNetCore.Mvc;
using WebAPIDemo.Models;
using WebAPIDemo.Services;

namespace WebAPIDemo.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SensorDatasController : ControllerBase
    {
        private readonly SensorDataService _sensorDataService;

        public class BodyData
        {
            public string DeviceId { get; set; } = string.Empty;
            public int Version { get; set; }
        }

        public SensorDatasController(SensorDataService sensorDataService)
        {
            _sensorDataService = sensorDataService;
        }

        [HttpGet]
        [Route("~/api/AppVersion")]
        public IActionResult GetAppVersion()
        {
            return Ok("Version 1.0");
        }

        [HttpPost]
        [Route("~/api/PostVersion")]
        public IActionResult UpdateAppVersion([FromBody] BodyData data)
        {
            if (data != null)
            {
                Console.WriteLine("DeviceId: " + data.DeviceId);
                Console.WriteLine("Version: " + data.Version);
            }

            return Ok("Received");
        }

        [HttpGet]
        public async Task<List<SensorData>> Get()
        {
            return await _sensorDataService.GetAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<SensorData>> Get(string id)
        {
            var sensorData = await _sensorDataService.GetAsync(id);

            if (sensorData == null)
            {
                return NotFound();
            }

            return sensorData;
        }

        [HttpPost]
        public async Task<IActionResult> Post(SensorData sensorData)
        {
            await _sensorDataService.CreateAsync(sensorData);
            return CreatedAtAction(nameof(Get), new { id = sensorData.Id }, sensorData);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Put(string id, SensorData sensorData)
        {
            var oldData = await _sensorDataService.GetAsync(id);

            if (oldData == null)
            {
                return NotFound();
            }

            sensorData.Id = id;

            await _sensorDataService.UpdateAsync(id, sensorData);

            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(string id)
        {
            var sensorData = await _sensorDataService.GetAsync(id);

            if (sensorData == null)
            {
                return NotFound();
            }

            await _sensorDataService.RemoveAsync(id);

            return NoContent();
        }
    }
}
