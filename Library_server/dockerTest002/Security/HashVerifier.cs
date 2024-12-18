using System.Security.Cryptography;
using System.Text;

namespace dockerTest002.Security
{
    public class HashVerifier
    {
        public static string ComputeHmacSha256Hash(string input, string key)
        {
            var keyBytes = Encoding.UTF8.GetBytes(key);
            var inputBytes = Encoding.UTF8.GetBytes(input);

            using (var hmac = new HMACSHA256(keyBytes))
            {
                var hashBytes = hmac.ComputeHash(inputBytes);

                return BitConverter.ToString(hashBytes).Replace("-", "").ToUpper();
            }
        }
    }
}
