using Azure.Core;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using dockerTest002.Models;
using dockerTest002.Security;

namespace dockerTest002.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IConfiguration _configuration;
        private static readonly Dictionary<string, string> TokenStore = new();
        public static readonly HashSet<string> RevokedTokens = new();

        public AuthController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        [HttpPost("login")]
        public IActionResult Login([FromBody] UserLogin login)
        {
            string requiredSecretKey = _configuration["Jwt:Key"];

            if (string.IsNullOrEmpty(requiredSecretKey))
            {
                return StatusCode(500, new { Message = "Secret key is not configured" });
            }

            string expectedHash = HashVerifier.ComputeHmacSha256Hash("adammati", requiredSecretKey);

            if (!string.Equals(login.secret, expectedHash, StringComparison.OrdinalIgnoreCase))
            {
                return Unauthorized(new { Message = "Invalid secret" });
            }

            var token = GenerateJwtToken(login.user_id);
            TokenStore[login.user_id] = token;

            return Ok(new { Token = token });
        }

        [HttpGet("tokens")]
        public IActionResult GetTokens()
        {
            return Ok(TokenStore);
        }

        [HttpPost("revoke")]
        public IActionResult RevokeToken([FromBody] TokenRequest request)
        {
            if (string.IsNullOrEmpty(request.Token))
            {
                return BadRequest(new { Message = "Token is required" });
            }

            RevokedTokens.Add(request.Token);

            return Ok(new { Message = "Token has been revoked" });
        }

        private string GenerateJwtToken(string username)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(ClaimTypes.Name, username)
            };

            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(int.Parse(_configuration["Jwt:ExpireMinutes"])),
                signingCredentials: credentials);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
