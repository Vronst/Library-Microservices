using Microsoft.EntityFrameworkCore;
using pro_sec_proj_test6.Models;

namespace pro_sec_proj_test6.Models
{
    public class ConfConnDB : DbContext
    {
        public ConfConnDB(DbContextOptions<ConfConnDB> options) : base(options) { }
        public DbSet<Ksiazka> Ksiazka { get; set; }
    }
}
