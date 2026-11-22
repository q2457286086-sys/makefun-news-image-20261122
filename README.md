# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/q2457286086-sys/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/q2457286086-sys/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday, 22 November 2026:
a newspaper front page with the day's four biggest stories and four more
in brief. Russian missiles land in Poland and NATO calls it a violation;
Trump, Xi and Putin talk nukes with no breakthrough; the Houthis launch
revenge strikes on the Saudi capital; COP31 reaches its final day with
the deal still short. Every headline was checked against news reports
dated 22 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That copies `entry.png` to `out/entry.png`. The program runs with no
network and writes the same bytes on every run.

## How the image was made

`draw_frontpage.py` draws the front page with Pillow: a masthead naming
the day, the four main stories in a 2x2 grid, a briefs band and a footer.
The illustration strip (`hero.png`) is an AI-generated editorial
illustration of NATO jets scrambling at dawn over Poland, drawn with no
text in it, so every word the judge reads comes from the script's own
lettering — nothing garbled, nothing invented. Run it again to rebuild
the image:

```sh
python3 draw_frontpage.py
```

## Files

| File | What it is |
|---|---|
| `main.ts` | Entry point: copies `entry.png` to the output directory. |
| `entry.png` | The image: 1024x1024, the day's news as a front page. |
| `draw_frontpage.py` | The script that draws `entry.png` from `hero.png`. |
| `hero.png` | Editorial illustration for the front page (jets over Poland). |

---

<sub>Entered on [make.fun](https://make.fun/?ref=1d9qr14r&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
