# Star Wars Opening Crawl - Improved

index Run
indexbash
python star_wars_crawl.py

1 = Default Umbra story, 2 = Type your own, 3 = Load .txt
index
**Tip:** Fullscreen terminal + large font = best effect. Ctrl+C to stop.

index What Was Fixed

| Original Bug | Fix |

|---|---|
| Flickered - cleared screen 3x per frame | Single redraw per frame |
| Printed whole text, then scrolled weirdly | Real bottom-to-top scroll |
| No perspective, no colour, no centering | Yellow + centered + top lines indented = perspective illusion |
| Hardcoded text only | Menu: default / type your own / load `.txt` |
| No Ctrl+C handling | Clean exit: "May the Force be with you." |
| No intro | Added "A long time ago..." + STAR WARS title card |

index How Perspective Works
index
Bottom line: full width, no indent  -> close
Top line:    indented + narrower    -> far away
Each frame: shift all lines up by 1
index

index Make Your Own Crawl
Create `my_crawl.txt`:
index
Episode V

MY STORY

In a classroom far, far away...
index
Then choose option 3.

index Requirements
None - only Python standard library.
