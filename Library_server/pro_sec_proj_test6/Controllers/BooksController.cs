using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using pro_sec_proj_test6.Models;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace pro_sec_proj_test6.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BooksController : ControllerBase
    {
        private readonly ConfConnDB _confConnDb;

        public BooksController(ConfConnDB confConnDb)
        {
            _confConnDb = confConnDb;
        }

        // GET: api/Books
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Ksiazka>>> GetBooks()
        {
            return await _confConnDb.Ksiazka.ToListAsync();
        }

        // GET: api/Books/{id}
        // GET: api/Books/0?title=...
        // GET: api/Books/0?author=...
        [HttpGet("{id}")]
        public async Task<ActionResult> GetItem(int id, bool? av, string title = null, string author = null, string genre = null)
        {
            if (id > 0)
            {
                var bookById = await _confConnDb.Ksiazka.FindAsync(id);

                if (bookById == null)
                {
                    return NotFound();
                }

                return Ok(bookById);
            }

            IQueryable<Ksiazka> query = _confConnDb.Ksiazka;

            if (!string.IsNullOrEmpty(title))
            {
                query = query.Where(b => b.Tytul.Contains(title));
            }

            if (!string.IsNullOrEmpty(author))
            {
                query = query.Where(b => b.Autor.Contains(author));
            }

            if (!string.IsNullOrEmpty(genre))
            {
                query = query.Where(b => b.Gatunek.Contains(genre));
            }

            if (av.HasValue)
            {
                query = query.Where(b => b.Dostepnosc.Equals(av));
            }

            var books = await query.ToListAsync();

            if (books.Count == 0)
            {
                return NotFound();
            }

            return Ok(books);
        }

        // POST: api/Books
        [HttpPost]
        public async Task<ActionResult<Ksiazka>> PostBook(Ksiazka book)
        {
            _confConnDb.Ksiazka.Add(book);
            await _confConnDb.SaveChangesAsync();

            return CreatedAtAction("GetItem", new { id = book.KsiazkaID }, book);
        }

        // PUT: api/Books/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutBook(int id, Ksiazka book)
        {
            if (id != book.KsiazkaID)
            {
                return BadRequest();
            }

            _confConnDb.Entry(book).State = EntityState.Modified;
            await _confConnDb.SaveChangesAsync();

            return NoContent();
        }

        // DELETE: api/Books/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBook(int id)
        {
            var book = await _confConnDb.Ksiazka.FindAsync(id);
            if (book == null)
            {
                return NotFound();
            }

            _confConnDb.Ksiazka.Remove(book);
            await _confConnDb.SaveChangesAsync();

            return NoContent();
        }
    }
}
