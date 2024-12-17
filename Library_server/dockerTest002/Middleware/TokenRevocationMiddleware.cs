using dockerTest002.Controllers;

namespace dockerTest002.Middleware
{
    public class TokenRevocationMiddleware
    {
        private readonly RequestDelegate _next;

        public TokenRevocationMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            var authHeader = context.Request.Headers["Authorization"].FirstOrDefault();
            if (authHeader != null && authHeader.StartsWith("Bearer "))
            {
                var token = authHeader.Substring("Bearer ".Length);

                if (IsTokenRevoked(token))
                {
                    context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                    await context.Response.WriteAsJsonAsync(new { Message = "Token has been revoked" });
                    return;
                }
            }

            await _next(context);
        }

        private bool IsTokenRevoked(string token)
        {
            return AuthController.RevokedTokens.Contains(token);
        }
    }

}
