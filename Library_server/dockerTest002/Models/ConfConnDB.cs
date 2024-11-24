using Microsoft.EntityFrameworkCore;

namespace dockerTest002.Models
{
    public class ConfConnDB : DbContext
    {
        public ConfConnDB(DbContextOptions<ConfConnDB> options) : base(options) { }
        public DbSet<Ksiazka> Ksiazka { get; set; }
    }
}
