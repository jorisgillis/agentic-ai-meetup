# Output format

Issues are grouped into named categories. Within each category, each
issue has a bold `file:line` header with a one-line description,
followed by a fenced diff block showing context.

## Example

---

## Naming Conventions

**`main.py:12`** — camelCase function name, should be `snake_case`
```diff
  DB_PATH = 'todos.db'
  app = FastAPI()
- def getDb():
+ def get_db():
      conn = sqlite3.connect(DB_PATH)
      conn.row_factory = sqlite3.Row
```

**`main.py:25`** — ALL_CAPS is reserved for module-level constants, not functions
```diff
  conn.close()
- def FETCH_ALL_TODOS():
+ def fetch_all_todos():
      conn = getDb()
      rows = conn.execute('SELECT * FROM todos ORDER BY created_at ASC').fetchall()
```

---

## Dead Code

**`main.py:10`** — `_cache` is declared but never read or written anywhere
```diff
  templates = Jinja2Templates(directory='templates')
- _cache = []
  
  def getDb():
```

**`main.py:73`** — `unused_variable` is assigned but never used
```diff
      conn.commit()
      conn.close()
-     unused_variable = 42
      todos = FETCH_ALL_TODOS()
      return renderItemsHtml(request, todos)
```

---

## Error Handling

**`main.py:51`** — bare `except: pass` silently swallows all exceptions including `KeyboardInterrupt`
```diff
      try:
          if title:
              conn.execute('INSERT INTO todos ...')
              conn.commit()
-     except:
-         pass
+     except Exception:
+         conn.rollback()
+         raise
      finally:
          conn.close()
```
