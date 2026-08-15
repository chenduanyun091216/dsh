#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态资源与配置常量 (从原 dsh_app.py 拆分)
========================================
- WHALE_ICO_B64 / WHALE_SVG_URI : 鲸鱼图标 (多尺寸 ICO / SVG data URI)
- PAGE_HTML                    : 安装器界面 (HTML/CSS/JS, 与进度条同窗口)
- INJECT_TITLEBAR_JS           : 注入 Harness 页面的自绘标题栏 + 账户宠物面板 JS
- NOFLASH_SCRIPT               : 消除跳转白闪的文档创建脚本
- APP_NAME / AUTHOR / DSH_URL / DSH_ACTUAL_URL / NODE_MIN / NPROC / DS_PRICES 等常量

本模块为纯数据, 不 import 本包其它模块。
"""

# ============================================================
# 鲸鱼图标(由 DSH 官方 favicon.svg 生成; _embed_icons.py 注入):
# WHALE_ICO_B64  -> 黑色鲸鱼多尺寸 ICO(任务栏图标 / 打包用)
# WHALE_SVG_URI  -> 白色鲸鱼 SVG data URI(自绘标题栏徽标)
# ============================================================
WHALE_ICO_B64 = "AAABAAcAEBAAAAAAIACgAQAAdgAAABgYAAAAACAAkgIAABYCAAAgIAAAAAAgAIgDAACoBAAAMDAAAAAAIACVBQAAMAgAAEBAAAAAACAAvgcAAMUNAACAgAAAAAAgAKYPAACDFQAAAAAAAAAAIACLCAAAKSUAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQAAAWdJREFUeJyF071L1WEUB/DPVSvSQUIsHIIcnJ3EIrdokbamNmlyaQhC+wOERiFoaLU1ehmjLYiaJFCopKJBFyE0wSHLrpzreeK5l3vtwOGc33PevuflRzv1YQCNHt9FdqX+k4y9ghtV8CEmcAczOIWfWMcSNhPR316Vb6OJfWylHvwIT/EWnzDXDfGtdH6CISyn8zhu4lfaA8nZzuDRrPqieruKQUxWSII3cD5bj3ZatJj9F8Pp4+fWDD5n4G/spv447f9QvMHrDD5THrOdUvlGwo9E2ziX/o1wXMPdKvBiDq2ZyJ5jtkIQPF2h9AwvMY8V7KTTn5RfU/+ChVzjQgkOutYxqNJzQRDyW8J+UPms4lIrAx52SRJ8gPcYS9jNXOn31F9FcFnHfXzEHn5Uu59K+71sL+5iGJfjXjrvO5JdyMojuI4PeIcreTP1vbTR/36m2i8Kh+zrRFB2G9DLtcXUg4ut7Wc6AroNZNryk4CrAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAACWUlEQVR4nMWVT4hPURTHP28eoSQyTc2kSSYs1JSFxpRkMUrJn4VSbFjJ1g57G2XEYmymWWBhoygWiCQLdkpqdvJnQfIvY5jfn6czfc9z3N97M42SU7d33z33nj/f873nwj+WbA5dLn0bKDTvkq6ltb9y0CWj80keHKN5ez4HuaIz2QHsAgaBbuAr8Ap4ANwEvrBAWaTvEPBQERU14zWwF9gE7Af2KJCqoP8wfgSYlpFvwH0Z+6m1N8AxYJ/mXgsbdwRvhwODxeRw2Hwb2Kj1W1q7C/Rr/2OtteRoBFhSF70tDgBTOjQRdN3AC+BkCMThawBN4AdwNAm2Qy7r0FPBlWlzHuAzOa19MzLeCFkP1TlZI0ZYusNJTQj8H1QtGuFuFHJUCLZ4V0o5pA2WehpBrgOG77PAdfteAS4lTrZV2OCMDh1XBA6RZ5EB1wI0xrJJ6XZrfVo2RisQ4II2bZFicdD1BhbNCMbnwClgLfBO0Ttdn4TalZ48vUnN3fABsadXBhwuY9tb0bZH+41JS1XPVmK7rIFxfwy4B3yqKGJRMQyag7rJ9v9Z/yvlZLbgq4H3FYebCVuKhP/fgZ0ydDXovJWY01JOSDFVQcMijHaI3HqQyXmteTspgq3ZbuDYXk+iTEdT+L4Etsv4KuBDgPGR7pTbueg0dFqeU+p1mLeADQHf9WKX6W7ovli/2gqMG6u8OWXhhRrQW2CHVwjPPrXnflH0rKK2DD4K4tGKx2pdrIP3nzpZBmxWz/GsUfteHtqE28nmejI7+gm/78hCpMpOrXiE6aEy2v8ivwBt9tgQrXYfDAAAAABJRU5ErkJggolQTkcNChoKAAAADUlIRFIAAAAgAAAAIAgGAAAAc3p69AAAA09JREFUeJzll1mIjWEYx39nMcKgZIkxWbLeSVkaMcyFGjeWaJS1KFEkTBTJvXLpilJKyZKLkWxpJgppEkJZb6xlX2fmnBm9p/+TZz7nO4uUi3nq6z3f+z7v+/yf/7N874GeLokSdZIau/Qk3N7w3qnxn4NLlaGf+lsj+SQpr4L0BWYDs4BxwDDgJ/AKeAJcA1rcvqRjyuay5TCU0lgJ7JWRriLPPWAN/4CBNJCRt4eASZF1izfS6+1+B6AXxcxMrQX9Z8Bu4L3Lo7yS1rhcB3oPm4GTwFfR2aH5u8Aihakhhp0AaLxL5oK0L9Omdo23gRqnd8sdfBQYqPkNmssoPwLAcwKXLlZxSY2T3eZw2AnlgW1eovlA5Ua33+azCo8l3Fm3N9Zzn7ktzrvz/JYKjXOB/UC1Y20M8DFi2JgI4zGnW1AWOC9eA0OK9AFLvssRg52uKVkYV5cC4pTbuFZzFjuThOaMkU3St5B5BuzdHBoQ6Z7dZJCUulRKvVzrjUrK5ct3ee69bgO+ORAGbkuMUzmZ49DvK6BoxkPJtUaoD88d9Y0RzqEOgWstxMA6R9m0mNgboED/mYh3n4G3wFbp1KiarCoM6AStJ/NVQJA3wH3nUVKGEzqgCrgALNS7gQwAnstgSM4jGo1V050h/T9Kcr0UrxbI1hXAywjtZiAYrwWGApciFeCZOhBJ4pykFS//nlEijgXmAyuB6VrPOoAWz2B4BzAFGOn2X1ennCi9Sq2Zk+GsnFSJxhCvR+r7jx1y3+WKfRXN89Cwgix1+0OSrnKNrFtCNsUc2JGnvuP02vR7u87sD5zO0yVD52yMhrvW1XGmDI+t+xlbe3RehT5GljOm41ndacYNxWEHohTD/i4Ynl0uyxtcSDpj2PoCjLJYBBB9gCsOtdFvnc6otAPt/Z0SFSUfujtk1S2D7gPgeB4HthFJiH6q41Ji3i4jdY52O+eGAxoSvF7zU6XfqP1NPhF9Vs4TkIfABx32A3gBfIqAqRODKddkmrUWzhgdTThJvS4y3SR6eQibBquWq8VQqPXNQv8UuAkM114LwUEBjeZZUr/zfpS8mEfFpEKgDLSN4fq+uMidImcjUcSArft/QcaSJeZ/lUTMJ7bcf1X0XPkF3MprkkDm/T4AAAAASUVORK5CYIKJUE5HDQoaCgAAAA1JSERSAAAAMAAAADAIBgAAAFcC+YcAAAVcSURBVHic7ZlpiFxFEMd/M+PGBBNU1PUgm6DxiEFciReKuOiiCEYRRPFAiBKEgCgkoCIqLOoHvyyeYIKgIggq6gdvkRDB9UKIUdRNPBKNRmNI4n3szpuRlir9p+335r3djYhOQTPz3nTX1f+qruqBLnXp/021Sa6td+DRAto2/hVUAxo2qlDDjN0lClVRIpPnvYAFwNHAgcAce78d+Bz4BlgPfAj8LDx8V/4xcqgEmgacCzwCbBF4FI1PgTuBYxM7slvOmAy0dyKFygXAe5FywZvjOaMZxUB4twI4gCmkWgnI9Jrg8+x9Zor5+noBvpvmUaUAsYttB08B+oEemb8WeMwgWJso3FzoALDBmDRldIJNywxtm8JPAEPAIHCvvfffU+NNk1+fjPJnAL/K9qvAYNRKYDnwligdK/YQcJDwPhH4RHZx3IZC7SPgmij2KmP+TOCXyPPh+w/GfA9Zc0gUD+H7GHBVxPtqUVQVbhnfV4ElwCybXzmQ3dqjxPOZKP++pUyn3c3gu23ObzZvFDhJ5gRalICWOyd8PpnjyMoHVBD4bsLzLwF7CsTc2F7xehj32/mgyi+0c6CZg/vMxnU23wN6Qri/WTDvyr8BTI884wbsZ5h9Fjg14lc3OIxG3i4K+LMjOaXI65l55imHTWapbnYHptMSvNwhD4pDirJWZiNkrLlVA9iFDSe8f2E0p8gJbmAjwn0n5dvRDr3QwWFJClnlK8kg4fPpksprtnDPhXjZlAhahY1motiIRVWNOEsYZOa1hRLcZSmGTgr3alCWMCAY9rbxKQ2jYVvo6XNVVQai/KUF0HGv/wjsKIiHtp1FlHXgKlvkufyiKBg7kQs5FPheTlpVvCmncyi/9wVuT+yUG/5wWQNmABuFwbeSy8uchi5gH2BdhzpnJFq7NLFbbvjXcvYU6jHXttQZPFcBPr5DwZsvJ7zpygQHfQfcJak3rNmcE+j+PBg56W9UT/StIyUM8LQZlD3M6phBe1ZhXnbfY4E5YGtDprvDoNRKyPJ1odzuuAN9Vky5EedH3nXyjKTvQ6xsK8g47pwvrUQJ3VygGxPQyRLp9KkycaAQCgKPE0X9MzbmcGsr89Jh/F7LjBsiJVsJ4zMpIHvMebWiQ+wzYZbX8gVjTgPuA34SQakDKd6B4P0HgDWRgpnM3SSG+PvNpp87M5dekYUrbauPNAxeYRj+IOfUrDpcOe0xQu8w0zyu0Poi0jP3HmooakiKPBp3UGWV1q7O5ay1/sPpens/JrJCpXsTcHxkyE50TIRHxae3fUU9bJXhvN+xVOoK7Q88X1A/ta3Z74uN8G1ZPUlolBnu+TXWS2D4ni19Q6o+Go/iItxk/GmEB8dAJGRXKb/F8n+gHjNgRKBTxGNMLhVm6S64EStKMqo6xgQ286OWc2mBzFSW83nXkqjjZ0hPPFVGuAKvCWwaIvP1xFkQPzuMxiXAP5ZW9y88WZCsFyOqZhxVwtvTYWnWXflAcxKQ9Yr4UeAyYGuCt/cNJ6sBCqU+ORt8gTc72k35d+9pYyHh8xZxkDvJP/sTBrftTqpfbj7OARbb3dKI8L8yNkCZB2OWWdQXQSNW2r3jvx8hwRo76nTBuvN4BjhBgjxFt9ncUFMlSQ+KvYHLgcct1W0TgS27SRi1UzMOtqbd5KnSyn+e7N5WuVbROVpEqhMuAQ7OM0AXKjXMoPlW9C2w54Y1QYHpi4l2cSihVBjTLRjbdq3oXi8q5SvfmXprWaW577X+YIntwECionRv3moG9Fb8K2pCf4S4Et7Q+Cnuo4oCLnymYL4yTdlfOQm+Wjl6UP8nqTaR2+gudalL/EG/AwyyLrHC4ncQAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAHhUlEQVR4nO1aa4hVVRT+7j13pqdmTQ+aEouoRMuwmDFGMpoKM3oQPaB/ZYmBFAkVFYEDQT8MKqggIkomogcVRZg2vf9kNagUOWVKVJKMqaOTWDPjmXtjw7ditdrn3H3OnJnRvAs2+86ZffZe33rttdc+QIMa1KAGNejwpdI4zambpRr7qvn7kBZAmc2BGc34bqQEUjvUBBCx16CPAnAmgFMAzABwBv/vxv4M4BeC3QRgj3k3mixBZKWyEd7pAG4H8DYBxgSR1vZQCC8CuB7AER7BHpQUqd9XAugGMOgBOEpBHFAt5vNRz/jvAXQBOM4j5DLXrXhaNE6x7D+kGToPwPsGQKwAihmntSrHimDkeR+Am5GdcgmhFDguUr7qtPQQgGYF1LpEFpJ57RyrANwDYD+AmQDOBTDH8O6E1wtgI4CdfFYbL5M/FcBao3GtTTF30Wo9K5B39Hy7AHwOYDWAYQAbCNDnMrq5uDObAnCCLIwq7NsAbOdiFlxIwPPFB/n9IQPoLAAncr3TqFXrYhJLRiigvxQv9xmeCwU/oMBbH66RmXcBLAfQSTfZxTHWEmQOFzjv9qx7MXeIWkJMsXP2A1gJoCUl+cpt9m0KfJygwVcZFC09bABX1e8fAbRznDPZI/n7DgB/eNbwtW+odZdvFEpl9ucr8JqZWGnwTiM0ZzVNTIbWme1QtPY6tQW1lTm6MUHA9pnbJeZyHaFKUZovEcixAL71aD72aLCihCaWs5jjRtQ7Tvv3GkHLe+0UdlKOoF1uO+MFmDwVmgNE7J/1+LwA+RrACQq8JgH0qXn3SwDz1Bh9WHImvCPQ7MWK9qotsbCsMWJ/iQe8MOas4viUhbUAxE8XK3PV70gG1+NZL63Fhpex5CD/kOyfLrlZb0DLfj3AuJAmdWHkbACXGQvR+7M8X5ERvN1J3jTz5aaI/W0pfn9LzsVsri5rzVUxIiR1tm2E/TIzby4qs/WaDC1WkTsLeDm8lBKCbBOzPCvsLE34dNvmWWPJAiOVgOgoLFHXJTQnF5RmigC7cpp+kit0GyyZqIn942ZS0UyXYT4v5TF9XybpC4quXaQsLBOVKITNKvjJwjsLSjGFsSncGUK2vDhQEDJulRF0JjqHWqkaK3h+LJN6rMyXX6Tt94MqG61nJUPcfZDHVW8y0pT0tT2vWSmqmDXSwOsD1nKeDl3StYiHniRLkDnvN2sG0yNqIhHC+gKSjIon1U0yZR2A7/LM9UXKrhGrjFOn2MH0hppIpLnSgMgL/iQAvwf6vWvfqfflkDObR+60gFjlGOfOCBVCmX2LeVZlVQacPA/4mD65mkIYTWGqqoLwDnXHICWup1QJLomqHNNhsAXRB8aXBsk0MrpAyZj97jqal+ebGGf6KLipCsCyFNP3xYFcu0GPSS97M56xNXCwTjCYMdPrY/+RuiNwBZl9gTmDCHMDd51SHgsYZr8m0Iws8FZWiCxT9ba7bQCeBvCAckddjQots9f4zjTFXxB9wpeH2D/mAScTltWFhFAzC5u/KeAhTIvZOvCa5qe4j60m2/+NUHghCoQA/InHVwl4+/hbg9R7cFVdiS1i/V7qgnIPGEKy/lKarTt3XADgKv6vakDI3Enz1zhPsAVU2LsIrGkWFxn2jG9l5beTd3pTFXNyCsxKTRSCBaPBx1y/nwlPxIBnheToT5PA1b1wvdxjun0Mjo+y9fDZfk8SErK/h7iDJGK2DD6qjuVOAY6OUaU0GS/jbvVgTFRMiVrszxBwJGHKU8jI0jR4XVA9us7ZwlnuVwBeopU2pwmhwr7bTGZvd7NcfBYFXoLdEgVA+G1l6V0LKS27XJgUGCP2nQlRdzKaBrVExYnIc1XnU4i+q9Q7xpMK878CpK3mxpMMfsSA13cPcxJuq9KaWLP7/ZzPHSL2lyb41ESCj422mkzVemNOHrVg5fuDik8IoUWLops+Dq9QDOrtzN43+kBWA9bYwnS7nOVabDybXkfMvuwp220NDHpxwP98W6X3YnS8hSBgdqu7B33xKdrvSLk7FM1vU8FRPtSw+YX07yWlyr6rcfGdopuY61pVz7N7dcgtkhzi3Kc709XhLs0CXN4zxVftcZKr8Ejs9s5XyFwR3wPZdRzYz5j7C1jHoI98xRDRfDOrTi+wkr2QCuzg/aHj+0IAV3ONUVaoZ6QxKJpo4bd8Woo2MbKBR56lpcmiiWuUj/tIzPQd815sEh19XZ+koHnqRsq1a9MEoBd3dAU/gxlK8eUkH7UfSWjfn19HAKKIZxRweXczj+GS6to7SPtNIWgRvXy/rZ4AZFLtlzOZl7/Fw9GA54C0l8/XsdxlNX+AfuuAvGbWsiSMP6jq/26el9VJ1CoriQTHNGUxwRR5Fok42XTWE1xbwHq+fEfgNHsdzxry/Y9ta1hP8JW0I2WBIsCt6kCUtfw15vhV9lSEQhdzBZQbWOX9GMAPAH6lpcxX89s5Sjz+bqEQnuD/ktwmhK9CviwR5qQQIk3fJcpivgUrTLzqkby7lPnCgiJBTCTpj57LddzLkghUyl3/Cyrl9N8J+Tr8YKXDGnyDGtSgBjUIBdLfR5xc1W2F70gAAAAASUVORK5CYIKJUE5HDQoaCgAAAA1JSERSAAAAgAAAAIAIBgAAAMM+YcsAAA9tSURBVHic7V1bjx1HEa45l/Vl10twbEc8ABLiN0AuhEuwYxxfhJ/yxkVRHIlbApJjQgRrRdgIBEHijYtQHngGszHxJQglxpD8BiTeeCCxjb3eDdjnzAW19BUq2j1zumd6Zvrs9ie1ZvecMzPdXdVV1dXV1UQRERERERERERERERERERERERERERERERERERGbEwlt7voXHdVjbpHMWT1HGnHTGfeNDG2U9xS0xZEEXK8ByrTid0v4jQk5EW1YMki6VZkhCZDoTBCJZSIaE9EJItoGYqnr00S0UPK8CRH9kojuGj6blDDIeKsxQxJIHYYa0dXIfpSIPkZEHyeiRwQjNMUGiD8BM6zjel2TDIoJMtrk6JMBhiBEIYj+MBF9moieIqJ9hnv00SltAhNSQ3tHJUzxFyJ6k4h+RUTXxO8T1DPCE1jMM/YQ0Qo6vdDKBETMBbM0LfysHM+fat+/S0RniOigphpCkJZzjQQdyVAdfIGI1jTiTD0S24UpUgMzXCSiA5rUiqgB2XEH0LGyo/sgelHBDFPof55qKgl1v2BkW4a3KZse3Mj70ZGsxzMh3otASyr+VkbiUaHGJFMnwr6QUs4GfM+mky5DMUc/ig40dWzoJYetwP+vCmKNKgxRNWPZhWtZUYZvr2hLBI1AZNVRvxMjZ1rinQsNhWEmUQj/w+tE9CMi+iO+U4TcTkTPoH0PoeQVjioCY/0c/fI2EV3C54lWh7kCN3g/EV0W4j6fk5E+tfy9atNxIjoJ6bbuoQ6rwrvZySDx+RI5Zz5CROeEg2fWfL1PZAb9qzuL7qJtO4noSSL6QImuZ9XGbmzb9/NoH8NOegl/V7nBgwI3eAQu5hFSV9fzPD0FEdgf4HvUT7T5/1kiegG+iTId/SQYgg1YX36KDATfEB7P0FXl/xFfjaLzaEwTwk8sOqop4VPxnMtE9HiFm3kBo3EHEX2fiP4j6uqLEaUP4s+wM4bzwAAm4k9qEl7XvWswipRIPG3wHTTpbL6uaOKfp2SszsaG9vn0SOrT4GtYA6F5mBb6In6qdcDZihH5OBhBjmCXcleM+v2iHabRNhTfc/vueCK8yeP4OU+LXXM38tX1BkbjbsO7xhiZbFQpvXzbUe/mgmHOi2eNS9rHn+/HlK9u++T7eQlaSrgL2poD923QSDwQX47gVeFmJRCbR2RiWDZW399yEMcsYaZQJTwjGZW0j0f+E5o7uOnIl1JuBYam3rbgdT67O0cNic9XNV20XXFjwhyFKLZRARMhYQ7j/qo59hDfHxZMausXqJJwt6HaDmozCyb83IBHzWpN4pfp4Fmcz9JAqYj38IzMQeSzaqny0w9w3Wn5DpvC/fOioR+DH+1VI9CV+GU62NZBxIRbsZgqTsV1RbxjaKnWXm3ow9ClXQ5dv32eF3240p9Ax7os32aOOrhqNfGGJlp1JssdRX6ZWvOp8/lZ54WKmavRz/PhRSK6oo0yG+KzHrUlSNnof6FE8phW69ioHHeg1goHVXBeMNvcMIEUvy4dxGI/FcTf1uD9p7X36/NpuV5PlqJ22ECt1WWCVa1dQYNF1qNY7dLnslXEZ1VxuGGDJQNMYaBJwt/Ad2zo2UbajBqotaZMwIwavD3AFXzDUfTrDW3C7Xzvd7R36ISX9Z0FqfevOLatSZED44ghsigocMWOORpGqWdRx6N5F+yAFVwl4V116lDT+2kHxNeN4vcw5QzS+6fPu+U0bhbxM0ylujB26jyfPW7HOhz5pn7K0U+LIRqFLvNuydlZi5zNsxEuSYM1DHb2ZJ6Wl+sU7lPVx0EZhTz6986Yd5eJ/mMBuzi5Tr8Xy7FFT4UH1joMUVm/XsGj6zmNU21EmurYYBoyQ/SnPRJfHzRXoAqCWBBi4l2y7Chd9LvEw3WFkER/UaIK1Iymd1UwFIEXtqMkin5qrAoyqNvdfbuKebHiZUvjj0X/GxoDhYQQRX9RIgW+16cUkGlY/im402b0f6pi63WfCFn0F5oUSBERvL8vI3ooNm/ahGHPw+gfBWT1F5ZSQEnfXqQAW/8vaxWyHf2hMYC+0BMy8QuxnP2Otq7RCfhFS6gAV2gW8XkvW6jEb3OhJ9fKXDuHmAH2iD1uuUVFnzMkfpjn+IXCkvBlz2sqZWRAy94ucwgwAV+0sP5zsZVqr+j0eY9fKBwIVGCgrCHgc80jE8jBJdvTCnSHTWpBTG7gbxDiPMb/oYj+DEutJz1vTM1FCjvltPkIEX2QiD5ERB9GxO/rIvlVU5ocQt92kqBqgGidixZczN8pZ1FI+r+NqN5CjHw9tM2EIZigyYyDpYx61wNdSFh++PuFbivT/9yoP+CeUFy+bUX1FiXE32bI9aM2jyp8TQuBr6sGVP2f7UINSAfQv2YwADdqBfeVZensEm1H9WYgyJEZxBigPy57qAPfe7mLUHJ++EHsuKlK3MSdcUi7t0+MW4zqzYXBO6xYrWMpsMdCirqqgX1tqgG5cvcYRBsbOzoK/PYm9BwFkEFzGzrpKMrUg7jMRIpYzg+ksocS2q/6QQenlv2KSHDdhGCJeMaXxTu8Q+pwZThVgTvj12hsn9Y/6/y70Mu/9WTx52KkS+b+d0Xe4CGIpZxOz6NPfBFLPfu+No1AyQA2Bl2Bnbl9JlHmUTjAdOyctqO4LnI8cxVlIJhgZ4XoH8DpdBZX/rwpmImewnObShXnjRcmnXRLbGvuw/kzMmxN95GBLMUzzgm1eE7zz+8ytLsLp9N6m33uOo3bqeXf7xKce5BX9w6jLr4CKBKDf19OkQeG+rDoPylyIPoC2wGLyD/I7/SKkaNu/BO4vMwYagNsYadYKz+F67TmVjMThrgeR6Zw/nuCqd1bmCGxp5HVw1CI/qwlqchtbw02KoA/O6nd0zbkNPOIllzCl6gtDPNv/TMZteszK5ptfS6C2b073lwfuNzxqM+w03cVHj7+rC3/wxB2zjVcLyN501XNKEyEGpq2WB+mz2ehfsum6LXholMKTIe68OpNxah/BUzAln8byEDE14joi8KZo1b6SLw3MRC/C2m4jtKLCpB5btqyRvV4Qh71VaLZt7W9VlIvThRJHrKi1albCvujlcU3Fz9AgYr4gsz6xUTejSnV30QoV9GByzmHjpVJq0gQeoq6dT3yE1E35akl31JQjjpOgliFpoRgycFJpNmhpDr360T0DREP16auN9VpAXP/4zg8ipM1P4i4xxOQgFlN4jOTj2pK0VmeWi/hYBzZkpeIyF2OYUqJNtIllrAAdVY7MKqv42Ny8feaiPiRv6kbX5CFGieoS4CBRaxdgdHC0iIteSZzPImRvgviTK2Zf1VLlsgHTPS1tyBBnRPDbIedPK7il/togBQ2alHprzjw8miHUq4UsrMHYIKlEkfEEkT0j2ccySpz3HNHPijOA9wp3iHFYgibShJcpSqsG/QqifsqVvVUsKfCR5GJlJ1JNmhly1iiHZmqxPG3K4ycKcQiH6Kg/v8FxBRBMpzAvQtwYY4NI4pHe0jBpD7B/acI/iXMHAh9kkHy/UMYwInFs07hmJoFg2ppDCb2KXFIg62OYl3JerNKl/mMoQ+x5CUZSqXdNER/20YOSW/gngr6NRpMfPM+i4gWDhsvO19nKr7f7AQvShJiygylo5LB9i2H7Ctc1pF19DRC+HWGaJRqxpUz29whM28lc0iIybOixZJZ1ywG0xniojjmRtLSGcyZz9ZQA1u5ZI4JMWU6es567nLuQVoifa9DMvDznQ1X5tYHRPTvVh3RRQ3iPzGj4zl6iET8YlOpyQwhmeGyOO/YeebAauDNOdhOPU/EH5ScquZzgEl7gs9DYvvD2n/B4uOT4kF9d/RmGfnDDuIH+NlZkwzlMj1slAJkHGnc0bPyIJs2rXRlW92pm6GcGUAtgEQpQPcQfwJPqE0SbD0lbdeGtZ6hfNh2kujNXu5oCzPbHJJT9TWr4vcec2ECrrxrmvjNXFIhUhdneN9CSk4l8zjudlnNbTPmfV7du6uW6/mDwJJT8QB2WlJuO9XKvHn4jgriJp6TbXbBxLlIRjmLge9pTJenaoTs4Rs6Jtvk3dRFYClp2d9jhS7P1QmlpOLqcuRNnWSbNozoo01cj2t1wtK6OFkrlDLB9YaFk6dpss1Z5a5n1ZvimQdcp4V9OjS6KmnJWv6wxWSbVUyYI/rqFXzmI+0N1+endSKdTC7NySYU+SuWp42a+ofjHm2SbdrU5zN45kviM85TyDuaXZbjZcYT3u3sBNO+OHaOzGvJap5nXMYAy5bJNsvKVMvBzMx4QGRxm1XK/Db82YbIZeCFCXyvbHUt9q80WUfXGOA+x0APE/EKuOKZAWSdDkFKvYb33CxJWCmZW2eA2+J01VqQhz/zgY5VnBdqSXFVq5/UMOuZDLC9VYMBciFNTb5705LuMkT5MhhvGf6HM2KvhV4HppEK/m0EGeBwWBwwJTs25JLiesHQ2XXA9+93jPTRcw/z6l1Z1LTtHF7ur5R10Y+oaYyxeOFp0bHsQQtVIkxwfd5TwmuWHj+zTBSpE55Dulzm6HqySo43lG05gvewY4slgAoq9QYpnkzGim61hsQAK6j3uEMJICXkDdRBnoTqK+XNUEhotnc28N4feHjHPS+UnXgQuujdks6f1pjCyMLBkXXtjgmuZzxJAGkD3BR1njXllMZYGyeIjjUm4HcfaDP5pHzwXoQtXzJYqWWE0YuNJ0xKGRsGyFGui5NOm9gBchZQNg1MDVNO6uDoWGaCx6BmVMYRhUGbL2UjRm4eXcY+wYdQqWegO3ljZlUKmg1BNMVkbyN503ZsttxdY+tZJqaznxdbv+X+RltwG5RV/ncwfiHqwO+6iileLrbkqd+1DZni5n//d7E3T0/7IrEk/Aq5YA4mMmOC/YgsthORvoWwKeJpdOwj2gbXqZYSV29zBsKoDOhfQMLsuijbY8nSYANG2VUwPu+p7AocIMoxDp1Ct1J97AY2PWcPdOs1CxWTo7DFrly4P4RU4Tq71of3WEo7g68/wfchZFkPAmVTGFPRf6s/Rw/RWhJeswuW9keB/fvbG7qD94CZeKSlSLB1QHhRg8Bm3J7NjKQnrmD742EQZQfyFWyHLfEWRPZZ8Zw6upltCLUi+E1IlwVc3wdpUPfZEQ4wOUV0LLaQ+5CNz/1izl1gvWHHJs+LECxMKmak/YY/80EcZrrvwlh9R8s2Ggy2OicmuLYhjlnX7xBh2RFbGIO+KxDRD5IoaSMiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiqFv8F9Y6n/HyoT1GAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAIUklEQVR4nO3d23LcNhIAUMKl//9lpPKQpBxZtmYIAn0553FrUx70jU1yJF0XAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8Nn4xf/GHvPmfy933KaI4jb4KnLMlxRHrWZ/hdyjCBo1/J8YCA1Jeu+m/4q6aEKif69T039FjRQmuZ9perXShgHwH42vbtrpPgA0/T3d6ye9rgnU+Gt1raP0uiVO4z+nWy2V0CVpGn+fLjVVQodkaf4zOtRWepWTpPHPq1xfJVRMkMaPp2KdlfDjqkXzxyQvQVWZzAqsR709kedxNVbh8Jq/Zt2dzOu4msh+UM1fp/Yi5nJcxWU9YMRi4b36i57LcRWW8XDRC4Z6xlXUx5WL5s/XHHIWWJbJpojOi/gEf6dxFZRhA8heOFmtLHg5DCr6AFA4+a9ychhY5LVG4eyj8fP2ScmvAmv+fTR/YxEn2ywQv9k49xnOnr1Hyh5uFotX1PNo/jPxCSfSQSs3y2yQ7yhnrNIPrQ48G8Tm9Bk1/5nYhBbhNeDpxuhQDFb+vXFJ4/QAiNT8VYtB8++JR0onB4Dmf5aVf1880vpo3vxVi0LzPx+HEk4EqGPz7zxz9+bX9IGDFaWAKjb/aJK739H8gW8BIhRQ1QKpei6a/izAE6re7owmw5vEA+B0AVW8Qv59Js0fq87S+dEgKaeafxY40+ncdfnMZQfA6d/tXvXKv0PmRsr82beq+gzgdOM/9RdsNP/ZHJTzo2ACTjf/Eyq+ttyh0llSDQDNv0bV25idDIEmtwDVGqXqa8sTqp4r5BeBTgS7UvNXfGtBkw1A8+dc9zs0f4cztrsFqHDld5+/jyHw4ADYHdzszR+l8bs1Rbfzlt4AohoJGr9zM3Q99yerCtHVP5/uTTBOf4AqG4DmJ6N5+gNEkO0WwNReQ/GLw5IBUOVXXXWi+cUj7QYABBkArv75uPqLS7oNwOq/huYXn2UDQDFBAdE3AFf/NQxscUo3ADT/GppfvJYOAAUFRUTdAFz91zCsxW3pAKjyhy460Pyk3QDgtHk1EG0AuPqv0aJ42TsAFFUO8iSWKTcAV38imldhkQYA95UuVs4NgKcLy9X/Ps3Py2wA0Hi4RhgArv73lS1Qzg8AxRWb/Ihz2g3A1f8ezU/qAQCZzKsYAyCvcsVIvAHwZJFZ/9+n+c+ZVyE2AGjs49C/6+rf9wo0GpwxDRtALpkb45U/ihrpD6hWy8NPDIA8Mhfdu80ceQiUHwBPFZyk9nI33+rlQTaAHLJe/Ss377wK2D0AKhfEU7IWmlwnYAOITfPzKAMgLs0fPw7zSs4AiCl9YZF7ADxRgO4Jv0fzs40NgMhDPsMwnFdiBkAsqYuJfHYNAOv/n2l+8djOBhCD5hePIwyA8zR/fvNK6tSPA5OraMbGz5wpLunt2ADc/+cu8vFCLmejuJTgFmC/TEX+q4Y30AsxAPbK1Py7ZY/NvBIyAPaZRT7zE+fIGJsSDIA9FDgt3wJ0v1+czc4wmsYoLRvAcxS2GIVnADyjY/O/evWvGKN5JeOLQM0LYBHNn5QBsE7H5nfPn5wBcF/1xl/5ILd6rNLxDOCe6gWt+Yt7cgOo/AqweuP/TfM3YAN4XYfmX6lbvOaViGcARRMbhJgFZwP4XhF3LGQ/2tuADeBrHZv+VzHwjr8wA+Azjf85Hk//IhAOGQ8mNdtbAEXMKmlqv/sGoOlpreMA0PQ9r8jy3nwAKIDea7ghsHkAvPMEefW/Tz9p7r8jqLYBaPreNP+Ldr7e6fiXY9ljBKubcSWxcwP4KvDeMdOi2SKKcAvgSs47NP4CfhaAbs2/Y3DMK4lR6TC0sKKBd9f0uIKKcAsAqZvozYET4jw2ADJ4olnmFceI/g9HCha9PNUc84pp6zDwEJDIQqzJlX8BjQFAx+aPevXfPgi+OwA6TmLO6d782z6vDYBoNP/GbcAAoMsDv2xX/l9Zfga/8JEouj3tDxEvGwARaP5Dg+3VAeBhIKtp/oNDwAbASZr/8BB4ZwDYAlhB8wcYAjYATtD8QYbAuwPAFsC7NH+gIWADYCcXjmDuDADJJIqq7/ofj4UNgF2s/gGHwN0BYAtAnSS2YgMwBDhVH1b/m7FxC8CTNH9wqwaALYD/14OaSLAFrNwAJJxddWD1X8QtACu5CMQzdw4ABdCX3Cf0xAagEPrZmXPr/8KYPXULYAj0IdeJeQbAHZo/uScHgOKo7UR+rf+LY/f0BmAI1OMdf6H63nELkD5I/Esui8Vk1zOA1EEiRA4jr//jymGefAiYJUj8zMr/vXpOGafdbwHSBag5+SoesxOvAVMFqKmUV7ONRpX4nfoeQIrgNCU364QfBKc/XOQHOx2drocMtTKSn2VES3iUxBKjHqLXyShw9hEx4VES3FWkWohaH6NIHEbEnwWIEFyIXp9LnytEGgCRgtxN9LifvvqPK55RcQCkeHJKK+OK63avRBwA/zAIUH/fMyoOgAwTmHpG0pobVQdA5qSwxo7cjwI1NqoOgEpJIpZRrKZeOkuFg59+QlxBhjp47MswRc3vnDvbBtBhgp/QbYiOpmcc3/k/VdCtoFeIXgtLvwFHr4AYCPnrYRY+2zGdgxLmJ7KCDamoNTELnuk4gVlfdHdjGmEQRK2LWew8xwlMbNG2lI4DuTTByePUMBiJYxDps4dU4TVgF6ded84gtyU8wADIOwg6Xt06nvlRAlrLbFAnM+FnDkuQaqv65ZmZ9HOH83H6A/Co8WITaZpmDIC+NDseAlL2L/PwDd4CkJUmX8AAoBqDAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuF71F4UfPpc2jF1EAAAAAElFTkSuQmCC"
WHALE_SVG_URI = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDUwIDUwIiBmaWxsPSJub25lIj48cGF0aCBkPSJNNDguODM1NCAxMC4wNDc5QzQ4LjMyMzIgOS43OTE5OSA0OC4xMDI1IDEwLjI3OTggNDcuODAzMiAxMC41Mjc4QzQ3LjcwMDcgMTAuNjA3OSA0Ny42MTQzIDEwLjcxMTkgNDcuNTI3MyAxMC44MDc2QzQ2Ljc3OTMgMTEuNjI0IDQ1LjkwNDggMTIuMTU5NyA0NC43NjIyIDEyLjA5NTdDNDMuMDkyMyAxMiA0MS42NjYgMTIuNTM1NiA0MC40MDU4IDEzLjgzOThDNDAuMTM3NyAxMi4yMzE5IDM5LjI0NzYgMTEuMjcyIDM3Ljg5MjYgMTAuNjU1OEMzNy4xODM2IDEwLjMzNTkgMzYuNDY2OCAxMC4wMTU2IDM1Ljk3MDIgOS4zMTk4MkMzNS42MjM1IDguODIzNzMgMzUuNTI5MyA4LjI3MTk3IDM1LjM1NiA3LjcyNzU0QzM1LjI0NTYgNy4zOTk5IDM1LjEzNTMgNy4wNjM5NiAzNC43NjUxIDcuMDA3ODFDMzQuMzYzMyA2Ljk0Mzg1IDM0LjIwNTYgNy4yODc2IDM0LjA0NzkgNy41NzU2OEMzMy40MTggOC43NTE5NSAzMy4xNzMzIDEwLjA0NzkgMzMuMTk3MyAxMS4zNTk5QzMzLjI1MjQgMTQuMzEyIDM0LjQ3MzYgMTYuNjY0MSAzNi44OTk5IDE4LjMzNTlDMzcuMTc1OCAxOC41Mjc4IDM3LjI0NjYgMTguNzE5NyAzNy4xNTk3IDE5QzM2Ljk5NDYgMTkuNTc1NyAzNi43OTc0IDIwLjEzNTcgMzYuNjI0IDIwLjcxMTlDMzYuNTEzNyAyMS4wODAxIDM2LjM0ODYgMjEuMTU5NyAzNS45NjI0IDIxQzM0LjYzMDkgMjAuNDMyMSAzMy40ODEgMTkuNTkxOCAzMi40NjQ0IDE4LjU3NTdDMzAuNzM5MyAxNi44NzIxIDI5LjE3OTIgMTQuOTkxNyAyNy4yMzM0IDEzLjUyQzI2Ljc3NjQgMTMuMTc1OCAyNi4zMTkzIDEyLjg1NiAyNS44NDY3IDEyLjU1MThDMjMuODYxOCAxMC41ODQgMjYuMTA2OSA4Ljk2Nzc3IDI2LjYyNyA4Ljc3NTg4QzI3LjE3MDQgOC41NzU2OCAyNi44MTU5IDcuODg3NyAyNS4wNTkxIDcuODk2QzIzLjMwMjIgNy45MDM4MSAyMS42OTUzIDguNTAzOTEgMTkuNjQ3IDkuMzAzNzFDMTkuMzQ3NyA5LjQyMzgzIDE5LjAzMjIgOS41MTE3MiAxOC43MDk1IDkuNTgzOThDMTYuODUwMSA5LjIyMzYzIDE0LjkxOTkgOS4xNDM1NSAxMi45MDMzIDkuMzc1OThDOS4xMDU5NiA5LjgwNzYyIDYuMDcyNzUgMTEuNjM5NiAzLjg0MzI2IDE0Ljc2ODFDMS4xNjQ1NSAxOC41Mjc4IDAuNTM0MTggMjIuNzk5OCAxLjMwNjY0IDI3LjI1NTlDMi4xMTc2OCAzMS45NTIxIDQuNDY1ODIgMzUuODM5OCA4LjA3MzczIDM4Ljg3OTlDMTEuODE1OSA0Mi4wMzIyIDE2LjEyNTUgNDMuNTc2MiAyMS4wNDEgNDMuMjgwM0MyNC4wMjY5IDQzLjEwNCAyNy4zNTE2IDQyLjY5NjMgMzEuMTAxNiAzOS40NTYxQzMyLjA0NjkgMzkuOTM2IDMzLjAzOTYgNDAuMTI3OSAzNC42ODYgNDAuMjcyQzM1Ljk1NDYgNDAuMzkyMSAzNy4xNzU4IDQwLjIwOCAzOC4xMjExIDQwLjAwNzhDMzkuNjAyMSAzOS42ODggMzkuNDk5NSAzOC4yODgxIDM4Ljk2MzkgMzguMDMyMkMzNC42MjMgMzUuOTY3OCAzNS41NzYyIDM2LjgwODEgMzQuNzEgMzYuMTI3OUMzNi45MTU1IDMzLjQ2MzkgNDAuMjQwMiAzMC42OTU4IDQxLjU0IDIxLjcyOEM0MS42NDI2IDIxLjAxNjEgNDEuNTU1NyAyMC41Njc5IDQxLjU0IDE5Ljk5MTdDNDEuNTMyMiAxOS42Mzk2IDQxLjYxMDggMTkuNTAzOSA0Mi4wMDQ5IDE5LjQ2MzlDNDMuMDkyMyAxOS4zMzU5IDQ0LjE0NzkgMTkuMDMxNyA0NS4xMTY3IDE4LjQ4NzhDNDcuOTI5MiAxNi45MTk5IDQ5LjA2NCAxNC4zNDM4IDQ5LjMzMTUgMTEuMjU1OUM0OS4zNzExIDEwLjc4MzcgNDkuMzIzNyAxMC4yOTU5IDQ4LjgzNTQgMTAuMDQ3OVpNMjQuMzI2MiAzNy44Mzk4QzIwLjExOTYgMzQuNDYzOSAxOC4wNzkxIDMzLjM1MjEgMTcuMjM1OCAzMy4zOTk5QzE2LjQ0ODIgMzMuNDQ4MiAxNi41ODk4IDM0LjM2ODIgMTYuNzYzMiAzNC45Njc4QzE2Ljk0NDMgMzUuNTYwMSAxNy4xODEyIDM1Ljk2ODMgMTcuNTExNyAzNi40ODc4QzE3Ljc0MDIgMzYuODMyIDE3Ljg5NzkgMzcuMzQ0MiAxNy4yODMyIDM3LjcyOEMxNS45MjgyIDM4LjU4NCAxMy41NzI4IDM3LjQzOTkgMTMuNDYyNCAzNy4zODM4QzEwLjcyMDcgMzUuNzM1OCA4LjQyODIyIDMzLjU2MDEgNi44MTM0OCAzMC41ODRDNS4yNTM0MiAyNy43MTk3IDQuMzQ3NjYgMjQuNjQ3OSA0LjE5Nzc1IDIxLjM2NzdDNC4xNTgyIDIwLjU3NTcgNC4zODY3MiAyMC4yOTU5IDUuMTU4NjkgMjAuMTUxOUM2LjE3NTI5IDE5Ljk2IDcuMjIzMTQgMTkuOTE5OSA4LjIzOTI2IDIwLjA3MThDMTIuNTMyNyAyMC43MTE5IDE2LjE4ODUgMjIuNjcxOSAxOS4yNTI5IDI1Ljc3NTlDMjEuMDAyIDI3LjU0MzkgMjIuMzI1MiAyOS42NTU4IDIzLjY4ODUgMzEuNzIwMkMyNS4xMzc3IDMzLjkxMjEgMjYuNjk3OCAzNiAyOC42ODMxIDM3LjcxMTlDMjkuMzg0MyAzOC4zMTIgMjkuOTQzNCAzOC43NjgxIDMwLjQ3OSAzOS4xMDRDMjguODY0MyAzOS4yODgxIDI2LjE2OTkgMzkuMzI4MSAyNC4zMjYyIDM3LjgzOThaTTI2LjM0MzMgMjQuNjAwMUMyNi4zNDMzIDI0LjI0OCAyNi42MTkxIDIzLjk2NzggMjYuOTY1OCAyMy45Njc4QzI3LjA0NDQgMjMuOTY3OCAyNy4xMTUyIDIzLjk4MzkgMjcuMTc4MiAyNC4wMDc4QzI3LjI2NTEgMjQuMDQgMjcuMzQzOCAyNC4wODc5IDI3LjQwNjcgMjQuMTYwMkMyNy41MTcxIDI0LjI3MiAyNy41ODAxIDI0LjQzMjEgMjcuNTgwMSAyNC42MDAxQzI3LjU4MDEgMjQuOTUyMSAyNy4zMDQyIDI1LjIzMTkgMjYuOTU3NSAyNS4yMzE5QzI2LjYxMDggMjUuMjMxOSAyNi4zNDMzIDI0Ljk1MjEgMjYuMzQzMyAyNC42MDAxWk0zMi42MDY0IDI3Ljg3OTlDMzIuMjA0NiAyOC4wNDc5IDMxLjgwMjcgMjguMTkxOSAzMS40MTY1IDI4LjIwOEMzMC44MTc5IDI4LjIzOTcgMzAuMTY0MSAyNy45OTIyIDI5LjgwOTYgMjcuNjg4QzI5LjI1ODMgMjcuMjE1OCAyOC44NjQzIDI2Ljk1MjEgMjguNjk4NyAyNi4xMjc5QzI4LjYyNzkgMjUuNzc1OSAyOC42Njc1IDI1LjIzMTkgMjguNzMwNSAyNC45MTk5QzI4Ljg3MjEgMjQuMjQ4IDI4LjcxNDQgMjMuODE1OSAyOC4yNDk1IDIzLjQyMzhDMjcuODcxNiAyMy4xMDQgMjcuMzkxMSAyMy4wMTYxIDI2Ljg2MzMgMjMuMDE2MUMyNi42NjYgMjMuMDE2MSAyNi40ODQ5IDIyLjkyNzcgMjYuMzUxMSAyMi44NTZDMjYuMTMwNCAyMi43NDQxIDI1Ljk0OTIgMjIuNDYzOSAyNi4xMjI2IDIyLjEyMDFDMjYuMTc3NyAyMi4wMDc4IDI2LjQ0NTggMjEuNzM1OCAyNi41MDg4IDIxLjY4OEMyNy4yMjU2IDIxLjI3MiAyOC4wNTI3IDIxLjQwNzcgMjguODE2OSAyMS43MTk3QzI5LjUyNTkgMjIuMDE2MSAzMC4wNjE1IDIyLjU2MDEgMzAuODM0IDIzLjMyODFDMzEuNjIxNiAyNC4yNTU5IDMxLjc2MzIgMjQuNTExNyAzMi4yMTI0IDI1LjIwOEMzMi41NjY5IDI1Ljc1MiAzMi44OTAxIDI2LjMxMiAzMy4xMTA0IDI2Ljk1MjFDMzMuMjQ0NiAyNy4zNTIxIDMzLjA3MTMgMjcuNjgwMiAzMi42MDY0IDI3Ljg3OTlaIiBmaWxsPSIjZmZmZmZmIi8+PC9zdmc+"


APP_NAME = "DeepSeek Harness 安装器"
AUTHOR = "Mr.Chen"
DSH_URL = "http://127.0.0.1:3080"
DSH_ACTUAL_URL = [DSH_URL]  # 实际服务地址(可能从 npx 输出解析到不同端口)
NODE_MIN = (24, 0, 0)
NPROC = [None]  # 由本程序启动的 npx/dsh 子进程

# DeepSeek 官方价目(每百万 tokens, 元): (输入缓存未命中, 输入缓存命中, 输出)
# 来源: https://api-docs.deepseek.com/zh-cn/quick_start/pricing/
# 仅用于"今日消费"的本地估算(≈), 实际扣费以官网账单为准。
DS_PRICES = {
    "deepseek-v4-flash": (1.0, 0.02, 2.0),
    "deepseek-chat":     (1.0, 0.02, 2.0),   # v4-flash 别名
    "deepseek-v4-pro":   (3.0, 0.025, 6.0),
    "deepseek-reasoner": (3.0, 0.025, 6.0),  # v4-pro 别名
}
DS_PRICE_DEFAULT = DS_PRICES["deepseek-v4-flash"]


# ============================================================
# 界面 HTML (同一窗口: 安装界面 -> 最终 Harness 页面)
# ============================================================
PAGE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>dsh · Mr.chen</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { height:100%; overflow:hidden; }
  body {
    font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;
    color:#e2e8f0;
    background:
      radial-gradient(1000px 620px at 12% -10%, rgba(45,212,191,.20), transparent 60%),
      radial-gradient(900px 700px at 108% 112%, rgba(103,232,249,.14), transparent 55%),
      radial-gradient(760px 520px at 50% 125%, rgba(13,148,136,.16), transparent 60%),
      linear-gradient(160deg,#0b1220 0%, #0f172a 48%, #060a12 100%);
    display:flex; align-items:center; justify-content:center;
  }
  body::before, body::after {
    content:""; position:fixed; border-radius:50%; filter:blur(90px); z-index:0;
    animation: float 12s ease-in-out infinite alternate;
  }
  body::before { width:420px; height:420px; left:-130px; top:-130px;
    background:radial-gradient(circle, rgba(45,212,191,.32), transparent 70%); }
  body::after { width:380px; height:380px; right:-110px; bottom:-110px;
    background:radial-gradient(circle, rgba(103,232,249,.26), transparent 70%);
    animation-delay:-6s; }
  @keyframes float { from{ transform:translate(0,0) scale(1); } to{ transform:translate(60px,44px) scale(1.18); } }

  .card {
    position:relative; z-index:1; width:900px; max-width:92vw;
    background:rgba(13,20,38,.74);
    border:1px solid rgba(94,234,212,.22);
    border-radius:22px; padding:34px 44px 22px;
    box-shadow:0 40px 100px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.06);
    backdrop-filter: blur(14px);
    animation: cardIn .5s ease both;
  }
  @keyframes cardIn { from{ opacity:0; transform:translateY(16px) scale(.98); } to{ opacity:1; transform:none; } }
  .card::before { content:""; position:absolute; top:0; left:26px; right:26px; height:3px;
    border-radius:0 0 4px 4px;
    background:linear-gradient(90deg, transparent, #2dd4bf, #67e8f9, #2dd4bf, transparent);
    background-size:200% 100%; animation: shine 3.2s linear infinite; }
  @keyframes shine { from{ background-position:200% 0; } to{ background-position:-200% 0; } }

  .logo-wrap { text-align:center; }
  .logo {
    display:inline-flex; align-items:center; justify-content:center;
    width:66px; height:66px; border-radius:19px; font-size:25px; font-weight:800;
    background:linear-gradient(135deg,#0d9488,#2dd4bf 55%,#67e8f9);
    color:#042f2e; letter-spacing:1px;
    box-shadow:0 10px 30px rgba(45,212,191,.35);
    animation: logoPulse 2.6s ease-in-out infinite;
  }
  @keyframes logoPulse { 0%,100%{ box-shadow:0 10px 30px rgba(45,212,191,.30); } 50%{ box-shadow:0 10px 44px rgba(45,212,191,.55); } }
  .logo img { width:42px; height:42px; display:block; }
  h1 {
    text-align:center; font-size:28px; letter-spacing:3px; margin-top:12px;
    background:linear-gradient(90deg,#cbd5e1,#ffffff,#cbd5e1);
    -webkit-background-clip:text; background-clip:text; color:transparent;
  }
  .author { text-align:center; margin:10px 0 22px; }
  .author .pill {
    display:inline-block; padding:4px 18px; border-radius:999px; font-size:13px;
    color:#a7f3d0; letter-spacing:1px;
    border:1px solid rgba(45,212,191,.35); background:rgba(45,212,191,.08);
  }
  .author .pill b { color:#2dd4bf; }

  #status {
    display:flex; align-items:center; justify-content:center; gap:9px;
    text-align:center; font-size:15px; min-height:24px; margin-bottom:16px; color:#cbd5e1;
  }
  #status .spinner {
    width:14px; height:14px; border-radius:50%; flex:none;
    border:2px solid rgba(45,212,191,.25); border-top-color:#2dd4bf;
    animation: spin .8s linear infinite;
  }
  @keyframes spin { to { transform:rotate(360deg); } }

  .bar-wrap { display:flex; align-items:center; gap:14px; }
  .bar {
    flex:1; height:16px; border-radius:9px; overflow:hidden; position:relative;
    background:rgba(30,41,59,.92); border:1px solid rgba(51,65,85,.65);
  }
  #fill {
    height:100%; width:0%; border-radius:9px;
    background:linear-gradient(90deg,#0d9488,#2dd4bf,#67e8f9);
    box-shadow:0 0 12px rgba(45,212,191,.5);
    transition:width .5s ease;
  }
  #fill::after { content:""; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(255,255,255,.30), transparent 55%); }
  .bar.indeterminate #fill { width:34% !important; animation: slide 1.15s ease-in-out infinite; }
  @keyframes slide { 0%{ margin-left:-34%; } 100%{ margin-left:100%; } }
  #pct { min-width:46px; text-align:right; font-family:Consolas,monospace; font-size:14px; color:#67e8f9; }

  #stage { text-align:center; font-size:13px; color:#7dd3fc; margin-top:12px; letter-spacing:3px; min-height:18px; }

  .term {
    margin-top:20px; background:rgba(2,6,23,.86); border:1px solid rgba(30,41,59,.9);
    border-radius:14px; height:252px; overflow:hidden; display:flex; flex-direction:column;
    box-shadow:inset 0 0 26px rgba(0,0,0,.35);
  }
  .term-title {
    display:flex; align-items:center; gap:7px; padding:9px 14px; font-size:11px;
    color:#64748b; letter-spacing:1px;
    background:rgba(15,23,42,.92); border-bottom:1px solid rgba(30,41,59,.85);
    font-family:Consolas,monospace;
  }
  .term-title .tdot { width:9px; height:9px; border-radius:50%; }
  .term-title .r { background:#f87171; }
  .term-title .y { background:#fbbf24; }
  .term-title .g { background:#34d399; }
  .term-title .tname { margin-left:6px; }
  #log {
    flex:1; overflow-y:auto; padding:10px 15px;
    font-family:Consolas,"Courier New",monospace; font-size:12.5px; line-height:1.75;
    color:#4ade80; white-space:pre-wrap; word-break:break-all;
  }
  #log .cmd { color:#7dd3fc; }
  #log .err { color:#f87171; }
  #log .dim { color:#64748b; }
  #log .ok  { color:#34d399; }
  #log::-webkit-scrollbar { width:8px; }
  #log::-webkit-scrollbar-thumb { background:#1e293b; border-radius:4px; }
  #log::-webkit-scrollbar-track { background:transparent; }

  .foot { text-align:center; margin-top:15px; font-size:12px; color:#475569; letter-spacing:1px; }
  .foot b { color:#2dd4bf; font-weight:600; }

  /* 自绘标题栏(无边框窗口) */
  .titlebar {
    position:fixed; top:0; left:0; right:0; height:42px; z-index:30;
    display:flex; align-items:center; justify-content:space-between;
    background:rgba(8,13,26,.92);
    border-bottom:1px solid rgba(94,234,212,.14);
    backdrop-filter: blur(10px);
    user-select:none;
  }
  .titlebar-left {
    flex:1; height:100%; display:flex; align-items:center; gap:8px;
    padding:0 14px; cursor:default;
  }
  .tb-logo {
    display:inline-flex; align-items:center; justify-content:center;
    width:24px; height:24px; border-radius:7px; font-size:11px; font-weight:800;
    background:linear-gradient(135deg,#0d9488,#2dd4bf); color:#042f2e;
  }
  .tb-logo img { width:15px; height:15px; display:block; }
  .tb-title {
    font-size:15px; font-weight:700; color:#cbd5e1; letter-spacing:.5px;
    font-family:"Palatino Linotype",Georgia,"Times New Roman",serif;
  }
  .tb-sep { color:#334155; }
  .tb-author {
    font-size:13px; font-weight:700; color:#f43f5e; letter-spacing:.5px; margin-left:-5px;
    font-family:"Palatino Linotype",Georgia,"Times New Roman",serif;
  }
  .titlebar-btns { display:flex; height:100%; }
  .tb-zoompct {
    min-width:46px; text-align:center; font-size:13px; color:#3b82f6; font-weight:600;
    font-family:Consolas,monospace; display:flex; align-items:center; justify-content:center;
    user-select:none;
  }
  .tb-btn {
    width:50px; height:100%; border:none; background:transparent;
    color:#94a3b8; cursor:pointer;
    display:flex; align-items:center; justify-content:center;
    transition:background .15s ease, color .15s ease;
  }
  .tb-btn svg { width:17px; height:17px; display:block; }
  .tb-btn:hover { background:rgba(148,163,184,.16); color:#e2e8f0; }
  .tb-btn:active { background:rgba(148,163,184,.28); }
  .tb-sep { width:1px; height:18px; background:rgba(148,163,184,.28); margin:0 4px; align-self:center; }
  .tb-close:hover { background:#ef4444; color:#fff; }
  .tb-close:active { background:#dc2626; }

  /* 无边框窗口拖拽缩放手柄 */
  .pwv-rz { position:fixed; z-index:29; }
  .pwv-rz-n { top:0; left:10px; right:10px; height:6px; cursor:n-resize; }
  .pwv-rz-s { bottom:0; left:10px; right:10px; height:6px; cursor:s-resize; }
  .pwv-rz-e { right:0; top:10px; bottom:10px; width:6px; cursor:e-resize; }
  .pwv-rz-w { left:0; top:10px; bottom:10px; width:6px; cursor:w-resize; }
  .pwv-rz-ne { top:0; right:0; width:12px; height:12px; cursor:ne-resize; }
  .pwv-rz-nw { top:0; left:0; width:12px; height:12px; cursor:nw-resize; }
  .pwv-rz-se { bottom:0; right:0; width:12px; height:12px; cursor:se-resize; }
  .pwv-rz-sw { bottom:0; left:0; width:12px; height:12px; cursor:sw-resize; }

  #modal { display:none; position:fixed; inset:0; background:rgba(2,6,23,.76);
    align-items:center; justify-content:center; z-index:10; }
  #modal.show { display:flex; }
  .dialog {
    width:500px; max-width:90vw; background:rgba(15,23,42,.97);
    border:1px solid rgba(94,234,212,.26); border-radius:18px;
    padding:30px 30px 26px; text-align:center;
    box-shadow:0 30px 80px rgba(0,0,0,.6);
    animation: pop .25s ease both;
  }
  @keyframes pop { from{ opacity:0; transform:scale(.92); } to{ opacity:1; transform:none; } }
  .dialog .qicon { font-size:34px; line-height:1; margin-bottom:10px; }
  .dialog p { font-size:15px; margin:6px 0 24px; line-height:1.9; color:#e2e8f0; white-space:pre-line; }
  .btn {
    border:none; border-radius:10px; padding:11px 32px; font-size:14px; cursor:pointer; margin:0 8px;
    transition:transform .15s ease, box-shadow .15s ease, background .15s ease;
  }
  .btn:hover { transform:translateY(-2px); }
  .btn.ok { background:linear-gradient(135deg,#0d9488,#0f766e); color:#fff;
    box-shadow:0 8px 22px rgba(13,148,136,.4); }
  .btn.ok:hover { box-shadow:0 12px 30px rgba(13,148,136,.55); }
  .btn.no { background:#1e293b; color:#cbd5e1; border:1px solid #334155; }
  .btn.no:hover { background:#334155; }
</style>
</head>
<body>
  <div class="titlebar">
    <div class="titlebar-left pywebview-drag-region">
      <span class="tb-logo whale-badge">DSH</span>
      <span class="tb-title">dsh</span>
      <span class="tb-author">@ Mr.chen</span>
    </div>
    <div class="titlebar-btns">
      <button class="tb-btn" id="btnZoomOut" title="缩小"><svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.6 10.6 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M5.2 7h3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></button>
      <span class="tb-zoompct" id="zoomPct">100%</span>
      <button class="tb-btn" id="btnZoomIn" title="放大"><svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.6 10.6 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M7 5.2v3.6M5.2 7h3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></button>
      <button class="tb-btn" id="btnZoomReset" title="重置为 100%"><svg viewBox="0 0 16 16"><path d="M13 8a5 5 0 1 1-1.4-3.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M13 1.8v3.2H9.8" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      <span class="tb-sep"></span>
      <button class="tb-btn" id="btnMin" title="最小化"><svg viewBox="0 0 16 16"><path d="M3 8h10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>
      <button class="tb-btn" id="btnMax" title="最大化"><svg viewBox="0 0 16 16"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></button>
      <button class="tb-btn tb-close" id="btnClose" title="关闭"><svg viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>
    </div>
  </div>
  <div class="card" id="card">
    <div class="logo-wrap"><div class="logo whale-badge">DSH</div></div>
    <h1>DeepSeek Harness</h1>
    <div class="author"><span class="pill">安装器 · 作者：<b>Mr.Chen</b></span></div>
    <div id="status"><span class="spinner"></span><span id="stext">正在初始化…</span></div>
    <div class="bar-wrap">
      <div class="bar" id="bar"><div id="fill"></div></div>
      <div id="pct">0%</div>
    </div>
    <div id="stage">准备中</div>
    <div class="term">
      <div class="term-title">
        <span class="tdot r"></span><span class="tdot y"></span><span class="tdot g"></span>
        <span class="tname">Terminal · 实时输出</span>
      </div>
      <div id="log"></div>
    </div>
    <div class="foot">DeepSeek Harness Installer · <b>Mr.Chen</b></div>
  </div>

  <div id="modal">
    <div class="dialog">
      <div class="qicon">🛠️</div>
      <p id="qtext"></p>
      <button class="btn ok" onclick="answer(true)">是</button>
      <button class="btn no" onclick="answer(false)">否，退出</button>
    </div>
  </div>

<script>
  function $(id){ return document.getElementById(id); }
  function setStatus(t){ $('stext').textContent = t; }
  function setProgress(v){
    var bar = $('bar'), fill = $('fill'), pct = $('pct');
    if (v < 0) { bar.classList.add('indeterminate'); pct.textContent = '…'; }
    else {
      bar.classList.remove('indeterminate');
      var n = Math.max(0, Math.min(100, Math.round(v)));
      fill.style.width = n + '%';
      pct.textContent = n + '%';
    }
  }
  function setStage(t){ $('stage').textContent = t; }
  function appendLog(line){
    if (typeof line === 'string') line = {text: line, cls: ''};
    var log = $('log');
    var div = document.createElement('div');
    if (line.cls) div.className = line.cls;
    div.appendChild(document.createTextNode(line.text || ''));
    log.appendChild(div);
    while (log.childNodes.length > 600) log.removeChild(log.firstChild);
    log.scrollTop = log.scrollHeight;
  }
  function showQuestion(text){ $('qtext').textContent = text; $('modal').classList.add('show'); }
  function getApi(){
    if (window.pywebview && window.pywebview.api) return window.pywebview.api;
    if (window.py) return window.py;
    return null;
  }
  // 鲸鱼徽标(由 _embed_icons.py 注入真实 data URI)
  var WHALE_URI = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDUwIDUwIiBmaWxsPSJub25lIj48cGF0aCBkPSJNNDguODM1NCAxMC4wNDc5QzQ4LjMyMzIgOS43OTE5OSA0OC4xMDI1IDEwLjI3OTggNDcuODAzMiAxMC41Mjc4QzQ3LjcwMDcgMTAuNjA3OSA0Ny42MTQzIDEwLjcxMTkgNDcuNTI3MyAxMC44MDc2QzQ2Ljc3OTMgMTEuNjI0IDQ1LjkwNDggMTIuMTU5NyA0NC43NjIyIDEyLjA5NTdDNDMuMDkyMyAxMiA0MS42NjYgMTIuNTM1NiA0MC40MDU4IDEzLjgzOThDNDAuMTM3NyAxMi4yMzE5IDM5LjI0NzYgMTEuMjcyIDM3Ljg5MjYgMTAuNjU1OEMzNy4xODM2IDEwLjMzNTkgMzYuNDY2OCAxMC4wMTU2IDM1Ljk3MDIgOS4zMTk4MkMzNS42MjM1IDguODIzNzMgMzUuNTI5MyA4LjI3MTk3IDM1LjM1NiA3LjcyNzU0QzM1LjI0NTYgNy4zOTk5IDM1LjEzNTMgNy4wNjM5NiAzNC43NjUxIDcuMDA3ODFDMzQuMzYzMyA2Ljk0Mzg1IDM0LjIwNTYgNy4yODc2IDM0LjA0NzkgNy41NzU2OEMzMy40MTggOC43NTE5NSAzMy4xNzMzIDEwLjA0NzkgMzMuMTk3MyAxMS4zNTk5QzMzLjI1MjQgMTQuMzEyIDM0LjQ3MzYgMTYuNjY0MSAzNi44OTk5IDE4LjMzNTlDMzcuMTc1OCAxOC41Mjc4IDM3LjI0NjYgMTguNzE5NyAzNy4xNTk3IDE5QzM2Ljk5NDYgMTkuNTc1NyAzNi43OTc0IDIwLjEzNTcgMzYuNjI0IDIwLjcxMTlDMzYuNTEzNyAyMS4wODAxIDM2LjM0ODYgMjEuMTU5NyAzNS45NjI0IDIxQzM0LjYzMDkgMjAuNDMyMSAzMy40ODEgMTkuNTkxOCAzMi40NjQ0IDE4LjU3NTdDMzAuNzM5MyAxNi44NzIxIDI5LjE3OTIgMTQuOTkxNyAyNy4yMzM0IDEzLjUyQzI2Ljc3NjQgMTMuMTc1OCAyNi4zMTkzIDEyLjg1NiAyNS44NDY3IDEyLjU1MThDMjMuODYxOCAxMC41ODQgMjYuMTA2OSA4Ljk2Nzc3IDI2LjYyNyA4Ljc3NTg4QzI3LjE3MDQgOC41NzU2OCAyNi44MTU5IDcuODg3NyAyNS4wNTkxIDcuODk2QzIzLjMwMjIgNy45MDM4MSAyMS42OTUzIDguNTAzOTEgMTkuNjQ3IDkuMzAzNzFDMTkuMzQ3NyA5LjQyMzgzIDE5LjAzMjIgOS41MTE3MiAxOC43MDk1IDkuNTgzOThDMTYuODUwMSA5LjIyMzYzIDE0LjkxOTkgOS4xNDM1NSAxMi45MDMzIDkuMzc1OThDOS4xMDU5NiA5LjgwNzYyIDYuMDcyNzUgMTEuNjM5NiAzLjg0MzI2IDE0Ljc2ODFDMS4xNjQ1NSAxOC41Mjc4IDAuNTM0MTggMjIuNzk5OCAxLjMwNjY0IDI3LjI1NTlDMi4xMTc2OCAzMS45NTIxIDQuNDY1ODIgMzUuODM5OCA4LjA3MzczIDM4Ljg3OTlDMTEuODE1OSA0Mi4wMzIyIDE2LjEyNTUgNDMuNTc2MiAyMS4wNDEgNDMuMjgwM0MyNC4wMjY5IDQzLjEwNCAyNy4zNTE2IDQyLjY5NjMgMzEuMTAxNiAzOS40NTYxQzMyLjA0NjkgMzkuOTM2IDMzLjAzOTYgNDAuMTI3OSAzNC42ODYgNDAuMjcyQzM1Ljk1NDYgNDAuMzkyMSAzNy4xNzU4IDQwLjIwOCAzOC4xMjExIDQwLjAwNzhDMzkuNjAyMSAzOS42ODggMzkuNDk5NSAzOC4yODgxIDM4Ljk2MzkgMzguMDMyMkMzNC42MjMgMzUuOTY3OCAzNS41NzYyIDM2LjgwODEgMzQuNzEgMzYuMTI3OUMzNi45MTU1IDMzLjQ2MzkgNDAuMjQwMiAzMC42OTU4IDQxLjU0IDIxLjcyOEM0MS42NDI2IDIxLjAxNjEgNDEuNTU1NyAyMC41Njc5IDQxLjU0IDE5Ljk5MTdDNDEuNTMyMiAxOS42Mzk2IDQxLjYxMDggMTkuNTAzOSA0Mi4wMDQ5IDE5LjQ2MzlDNDMuMDkyMyAxOS4zMzU5IDQ0LjE0NzkgMTkuMDMxNyA0NS4xMTY3IDE4LjQ4NzhDNDcuOTI5MiAxNi45MTk5IDQ5LjA2NCAxNC4zNDM4IDQ5LjMzMTUgMTEuMjU1OUM0OS4zNzExIDEwLjc4MzcgNDkuMzIzNyAxMC4yOTU5IDQ4LjgzNTQgMTAuMDQ3OVpNMjQuMzI2MiAzNy44Mzk4QzIwLjExOTYgMzQuNDYzOSAxOC4wNzkxIDMzLjM1MjEgMTcuMjM1OCAzMy4zOTk5QzE2LjQ0ODIgMzMuNDQ4MiAxNi41ODk4IDM0LjM2ODIgMTYuNzYzMiAzNC45Njc4QzE2Ljk0NDMgMzUuNTYwMSAxNy4xODEyIDM1Ljk2ODMgMTcuNTExNyAzNi40ODc4QzE3Ljc0MDIgMzYuODMyIDE3Ljg5NzkgMzcuMzQ0MiAxNy4yODMyIDM3LjcyOEMxNS45MjgyIDM4LjU4NCAxMy41NzI4IDM3LjQzOTkgMTMuNDYyNCAzNy4zODM4QzEwLjcyMDcgMzUuNzM1OCA4LjQyODIyIDMzLjU2MDEgNi44MTM0OCAzMC41ODRDNS4yNTM0MiAyNy43MTk3IDQuMzQ3NjYgMjQuNjQ3OSA0LjE5Nzc1IDIxLjM2NzdDNC4xNTgyIDIwLjU3NTcgNC4zODY3MiAyMC4yOTU5IDUuMTU4NjkgMjAuMTUxOUM2LjE3NTI5IDE5Ljk2IDcuMjIzMTQgMTkuOTE5OSA4LjIzOTI2IDIwLjA3MThDMTIuNTMyNyAyMC43MTE5IDE2LjE4ODUgMjIuNjcxOSAxOS4yNTI5IDI1Ljc3NTlDMjEuMDAyIDI3LjU0MzkgMjIuMzI1MiAyOS42NTU4IDIzLjY4ODUgMzEuNzIwMkMyNS4xMzc3IDMzLjkxMjEgMjYuNjk3OCAzNiAyOC42ODMxIDM3LjcxMTlDMjkuMzg0MyAzOC4zMTIgMjkuOTQzNCAzOC43NjgxIDMwLjQ3OSAzOS4xMDRDMjguODY0MyAzOS4yODgxIDI2LjE2OTkgMzkuMzI4MSAyNC4zMjYyIDM3LjgzOThaTTI2LjM0MzMgMjQuNjAwMUMyNi4zNDMzIDI0LjI0OCAyNi42MTkxIDIzLjk2NzggMjYuOTY1OCAyMy45Njc4QzI3LjA0NDQgMjMuOTY3OCAyNy4xMTUyIDIzLjk4MzkgMjcuMTc4MiAyNC4wMDc4QzI3LjI2NTEgMjQuMDQgMjcuMzQzOCAyNC4wODc5IDI3LjQwNjcgMjQuMTYwMkMyNy41MTcxIDI0LjI3MiAyNy41ODAxIDI0LjQzMjEgMjcuNTgwMSAyNC42MDAxQzI3LjU4MDEgMjQuOTUyMSAyNy4zMDQyIDI1LjIzMTkgMjYuOTU3NSAyNS4yMzE5QzI2LjYxMDggMjUuMjMxOSAyNi4zNDMzIDI0Ljk1MjEgMjYuMzQzMyAyNC42MDAxWk0zMi42MDY0IDI3Ljg3OTlDMzIuMjA0NiAyOC4wNDc5IDMxLjgwMjcgMjguMTkxOSAzMS40MTY1IDI4LjIwOEMzMC44MTc5IDI4LjIzOTcgMzAuMTY0MSAyNy45OTIyIDI5LjgwOTYgMjcuNjg4QzI5LjI1ODMgMjcuMjE1OCAyOC44NjQzIDI2Ljk1MjEgMjguNjk4NyAyNi4xMjc5QzI4LjYyNzkgMjUuNzc1OSAyOC42Njc1IDI1LjIzMTkgMjguNzMwNSAyNC45MTk5QzI4Ljg3MjEgMjQuMjQ4IDI4LjcxNDQgMjMuODE1OSAyOC4yNDk1IDIzLjQyMzhDMjcuODcxNiAyMy4xMDQgMjcuMzkxMSAyMy4wMTYxIDI2Ljg2MzMgMjMuMDE2MUMyNi42NjYgMjMuMDE2MSAyNi40ODQ5IDIyLjkyNzcgMjYuMzUxMSAyMi44NTZDMjYuMTMwNCAyMi43NDQxIDI1Ljk0OTIgMjIuNDYzOSAyNi4xMjI2IDIyLjEyMDFDMjYuMTc3NyAyMi4wMDc4IDI2LjQ0NTggMjEuNzM1OCAyNi41MDg4IDIxLjY4OEMyNy4yMjU2IDIxLjI3MiAyOC4wNTI3IDIxLjQwNzcgMjguODE2OSAyMS43MTk3QzI5LjUyNTkgMjIuMDE2MSAzMC4wNjE1IDIyLjU2MDEgMzAuODM0IDIzLjMyODFDMzEuNjIxNiAyNC4yNTU5IDMxLjc2MzIgMjQuNTExNyAzMi4yMTI0IDI1LjIwOEMzMi41NjY5IDI1Ljc1MiAzMi44OTAxIDI2LjMxMiAzMy4xMTA0IDI2Ljk1MjFDMzMuMjQ0NiAyNy4zNTIxIDMzLjA3MTMgMjcuNjgwMiAzMi42MDY0IDI3Ljg3OTlaIiBmaWxsPSIjZmZmZmZmIi8+PC9zdmc+";
  function initBadges(){
    document.querySelectorAll('.whale-badge').forEach(function(el){
      el.innerHTML = '<img src="' + WHALE_URI + '" alt="DSH">';
    });
  }
  initBadges();
  function answer(yes){
    $('modal').classList.remove('show');
    var api = getApi();
    if (api && typeof api.answer === 'function') api.answer(yes);
  }
  // 自绘标题栏窗口控制(最小化/最大化/还原/关闭)
  var _maxed = false;
  function setZoomPct(p){ $('zoomPct').textContent = Math.round(p) + '%'; }
  // 内容区缩放(仅页面内容, 标题栏不缩放)
  function applyZoom(z){
    z = Math.max(0.5, Math.min(2, z));
    var kids = document.body.children;
    for (var i = 0; i < kids.length; i++){
      var el = kids[i];
      if (el.id === 'pwv-titlebar' || el.classList.contains('titlebar') || el.classList.contains('pwv-rz')) continue;
      el.style.zoom = (Math.abs(z - 1) < 0.001) ? '' : z;
    }
    document.body.style.overflow = (Math.abs(z - 1) < 0.001) ? '' : 'hidden';
    setZoomPct(Math.round(z * 100));
  }
  function zoomBy(d){
    var api = getApi();
    if (api && api.zoomBy) api.zoomBy(d);
  }
  function zoomReset(){
    var api = getApi();
    if (api && api.zoomReset) api.zoomReset();
  }
  $('btnZoomOut').addEventListener('click', function(){ zoomBy(-0.1); });
  $('btnZoomIn').addEventListener('click', function(){ zoomBy(0.1); });
  $('btnZoomReset').addEventListener('click', function(){ zoomReset(); });
  function winControl(action){
    var api = getApi();
    if (api && typeof api.windowControl === 'function') api.windowControl(action);
  }
  function winMin(){ winControl('min'); }
  function winToggleMax(){
    _maxed = !_maxed;
    winControl(_maxed ? 'max' : 'restore');
    $('btnMax').innerHTML = _maxed
      ? '<svg viewBox="0 0 16 16"><rect x="3.5" y="5.5" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M6.5 3.5H12a.5.5 0 0 1 .5.5v5.5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'
      : '<svg viewBox="0 0 16 16"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';
    $('btnMax').title = _maxed ? '还原' : '最大化';
  }
  function winClose(){ winControl('close'); }
  $('btnMin').addEventListener('click', winMin);
  $('btnMax').addEventListener('click', winToggleMax);
  $('btnClose').addEventListener('click', winClose);
  document.querySelector('.pywebview-drag-region').addEventListener('dblclick', winToggleMax);
  // 自绘窗口拖拽(替换 pywebview 内置: 修复缩放(ZoomFactor)后拖动错位/顿挫)
  (function(){
    var region = document.querySelector('.pywebview-drag-region');
    region.addEventListener('mousedown', function(ev){
      if (ev.button !== 0) return;
      ev.preventDefault();
      ev.stopPropagation();  // 阻止 pywebview 内置拖拽
      var dpr = window.devicePixelRatio || 1;
      var sx = ev.screenX, sy = ev.screenY;
      var wx = window.screenX, wy = window.screenY;
      function move(ev2){
        var nx = Math.round(wx + (ev2.screenX - sx) / dpr);
        var ny = Math.round(wy + (ev2.screenY - sy) / dpr);
        var api = getApi();
        if (api && api.moveWindowTo) api.moveWindowTo(nx, ny);
      }
      function up(){
        window.removeEventListener('mousemove', move);
        window.removeEventListener('mouseup', up);
      }
      window.addEventListener('mousemove', move);
      window.addEventListener('mouseup', up);
    });
  })();

  // 无边框窗口拖拽缩放(边缘/四角手柄, Pointer 捕获保证拖出窗口外仍生效)
  var RZ_CFG = { n:{w:0,h:-1}, s:{w:0,h:1}, e:{w:1,h:0}, w:{w:-1,h:0},
                 ne:{w:1,h:-1}, nw:{w:-1,h:-1}, se:{w:1,h:1}, sw:{w:-1,h:1} };
  ['n','s','e','w','ne','nw','se','sw'].forEach(function(edge){
    var el = document.createElement('div');
    el.className = 'pwv-rz pwv-rz-' + edge;
    document.body.appendChild(el);
    el.addEventListener('pointerdown', function(ev){
      ev.preventDefault();
      el.setPointerCapture(ev.pointerId);
      var c = RZ_CFG[edge];
      var dpr = window.devicePixelRatio || 1;
      var sx = ev.screenX, sy = ev.screenY;
      var sw0 = window.innerWidth, sh0 = window.innerHeight;
      function move(ev2){
        if (_maxed) return;
        var nw = Math.max(1024, sw0 + c.w * (ev2.screenX - sx) / dpr);
        var nh = Math.max(618,  sh0 + c.h * (ev2.screenY - sy) / dpr);
        var api = getApi();
        if (api && api.resizeWindow) api.resizeWindow(nw, nh, edge);
      }
      function up(){
        try { el.releasePointerCapture(ev.pointerId); } catch (e) {}
        el.removeEventListener('pointermove', move);
        el.removeEventListener('pointerup', up);
      }
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerup', up);
    });
  });
  // pywebview 的 JS 桥在页面加载完成(NavigationCompleted)之后才注入,
  // 直接监听 DOMContentLoaded 调用 py.onLoad() 会因桥未就绪而失败,
  // 导致后台任务永不启动(界面卡在"正在初始化")。
  // 因此改用 pywebviewready 事件 + 轮询兜底, 确保桥就绪后再启动。
  function boot(){
    var api = getApi();
    if (api && typeof api.onLoad === 'function'){
      try { api.onLoad(); return; } catch (e) {}
    }
    setTimeout(boot, 100);
  }
  window.addEventListener('pywebviewready', boot);
  boot();
</script>
</body>
</html>
"""


# 注入到 Harness 页面的自绘标题栏:
# 使用 DSH 自身的 --dsw-* CSS 变量(背景/边框/文字/悬停), 主题切换自动同步变色,
# 变量缺失时回退为深色; 同时给应用内容加 42px 顶部留白, 避免遮挡。
INJECT_TITLEBAR_JS = r'''
(function () {
  function getApi() {
    return window.py || (window.pywebview && window.pywebview.api) || null;
  }
  try {
    if (document.getElementById('pwv-titlebar')) return;
    var href = location.href || '';
    if (href.indexOf('://127.0.0.1') < 0) return;

    var style = document.createElement('style');
    style.id = 'pwv-titlebar-style';
    style.textContent = [
      '#pwv-titlebar{position:fixed;top:0;left:0;right:0;height:42px;z-index:2147483000;',
      'display:flex;align-items:center;justify-content:space-between;',
      'background:var(--dsw-alias-bg-layer-1,var(--dsw-alias-bg-base,rgba(8,13,26,.96)));',
      'border-bottom:1px solid var(--dsw-alias-border-l2,rgba(94,234,212,.16));',
      'color:var(--dsw-alias-label-primary,#cbd5e1);',
      'font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;user-select:none;}',
      '#pwv-titlebar .pwv-left{flex:1;height:100%;display:flex;align-items:center;gap:8px;padding:0 14px;}',
      '#pwv-titlebar .pwv-logo{width:24px;height:24px;border-radius:7px;font-size:11px;font-weight:800;',
      'display:inline-flex;align-items:center;justify-content:center;',
      'background:linear-gradient(135deg,#0d9488,#2dd4bf);color:#042f2e;}',
      '#pwv-titlebar .pwv-logo img{width:15px;height:15px;display:block;}',
      '#pwv-titlebar .pwv-title{font-size:15px;font-weight:700;letter-spacing:.5px;',
      'font-family:"Palatino Linotype",Georgia,"Times New Roman",serif;}',
      '#pwv-titlebar .pwv-author{margin-left:-5px;font-size:13px;font-weight:700;color:#f43f5e;',
      'letter-spacing:.5px;font-family:"Palatino Linotype",Georgia,"Times New Roman",serif;}',
      '#pwv-titlebar .pwv-btns{display:flex;height:100%;}',
      '#pwv-titlebar .pwv-zoompct{min-width:46px;text-align:center;font-size:13px;',
      'color:#3b82f6;font-weight:600;font-family:Consolas,monospace;',
      'display:flex;align-items:center;justify-content:center;user-select:none;}',
      '#pwv-titlebar .pwv-btn{width:50px;height:100%;border:none;background:transparent;color:inherit;',
      'cursor:pointer;display:flex;align-items:center;justify-content:center;',
      'transition:background .15s ease;}',
      '#pwv-titlebar .pwv-btn svg{width:17px;height:17px;display:block;}',
      '#pwv-titlebar .pwv-sep{width:1px;height:18px;background:rgba(148,163,184,.28);',
      'margin:0 4px;align-self:center;opacity:.7;}',
      '#pwv-titlebar .pwv-btn:hover{background:var(--dsw-alias-interactive-bg-hover,rgba(148,163,184,.16));}',
      '#pwv-titlebar .pwv-close:hover{background:#ef4444;color:#fff;}',
      'html.pwv-shifted,html.pwv-shifted body{height:100% !important;margin:0 !important;}',
      'html.pwv-shifted body{padding-top:42px !important;box-sizing:border-box !important;',
      'position:relative !important;}',
      '.pwv-rz{position:fixed;z-index:2147482999;}',
      '.pwv-rz-n{top:0;left:10px;right:10px;height:6px;cursor:n-resize;}',
      '.pwv-rz-s{bottom:0;left:10px;right:10px;height:6px;cursor:s-resize;}',
      '.pwv-rz-e{right:0;top:10px;bottom:10px;width:6px;cursor:e-resize;}',
      '.pwv-rz-w{left:0;top:10px;bottom:10px;width:6px;cursor:w-resize;}',
      '.pwv-rz-ne{top:0;right:0;width:12px;height:12px;cursor:ne-resize;}',
      '.pwv-rz-nw{top:0;left:0;width:12px;height:12px;cursor:nw-resize;}',
      '.pwv-rz-se{bottom:0;right:0;width:12px;height:12px;cursor:se-resize;}',
      '.pwv-rz-sw{bottom:0;left:0;width:12px;height:12px;cursor:sw-resize;}',
      '.pwv-pet{position:fixed;right:18px;bottom:18px;width:54px;height:54px;z-index:2147482990;',
      'border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;',
      'background:linear-gradient(135deg,#0d9488,#2dd4bf);',
      'box-shadow:0 8px 24px rgba(0,0,0,.35);',
      'animation:pwv-bob 2.6s ease-in-out infinite;}',
      '@keyframes pwv-bob{0%,100%{transform:translateY(0);}50%{transform:translateY(-6px);}}',
      '.pwv-pet img{width:28px;height:28px;pointer-events:none;}',
      '.pwv-petpanel{position:fixed;right:18px;bottom:84px;width:300px;z-index:2147482990;',
      'max-height:calc(100vh - 140px);overflow-y:auto;',
      'background:var(--dsw-alias-bg-layer-1,rgba(15,23,42,.97));',
      'border:1px solid var(--dsw-alias-border-l2,rgba(94,234,212,.22));',
      'border-radius:14px;padding:14px;box-shadow:0 20px 60px rgba(0,0,0,.5);',
      'font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;',
      'color:var(--dsw-alias-label-primary,#e2e8f0);display:none;}',
      '.pwv-petpanel.show{display:block;}',
      '.pwv-ph{display:flex;align-items:center;justify-content:space-between;',
      'font-size:13px;font-weight:700;margin-bottom:10px;}',
      '.pwv-pc{border:none;background:transparent;color:inherit;cursor:pointer;font-size:12px;opacity:.6;}',
      '.pwv-pc:hover{opacity:1;}',
      '.pwv-row{display:flex;justify-content:space-between;align-items:center;',
      'font-size:12.5px;padding:5px 0;gap:8px;}',
      '.pwv-row .pwv-sub{font-size:11px;opacity:.6;text-align:right;}',
      '.pwv-row.pwv-grp{margin-top:7px;padding-top:6px;border-top:1px solid var(--dsw-alias-border-l2,rgba(148,163,184,.18));}',
      '#pwv-balance,.pwv-num{font-weight:700;color:var(--dsw-alias-accent,#2dd4bf);text-align:right;}',
      '.pwv-pbtns{display:flex;gap:6px;margin-top:10px;}',
      '.pwv-pbtn{flex:1;border:none;border-radius:8px;padding:7px 0;font-size:12px;cursor:pointer;',
      'background:var(--dsw-alias-interactive-bg-hover,rgba(148,163,184,.18));color:inherit;}',
      '.pwv-pbtn:hover{filter:brightness(1.15);}',
      '.pwv-link{background:linear-gradient(135deg,#0d9488,#2dd4bf);color:#042f2e;font-weight:700;}',
      '.pwv-note{font-size:10.5px;opacity:.55;margin-top:9px;line-height:1.5;}'
    ].join('');
    (document.head || document.documentElement).appendChild(style);

    var tb = document.createElement('div');
    tb.id = 'pwv-titlebar';
    tb.innerHTML =
      '<div class="pwv-left pywebview-drag-region">' +
      '<span class="pwv-logo"><img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDUwIDUwIiBmaWxsPSJub25lIj48cGF0aCBkPSJNNDguODM1NCAxMC4wNDc5QzQ4LjMyMzIgOS43OTE5OSA0OC4xMDI1IDEwLjI3OTggNDcuODAzMiAxMC41Mjc4QzQ3LjcwMDcgMTAuNjA3OSA0Ny42MTQzIDEwLjcxMTkgNDcuNTI3MyAxMC44MDc2QzQ2Ljc3OTMgMTEuNjI0IDQ1LjkwNDggMTIuMTU5NyA0NC43NjIyIDEyLjA5NTdDNDMuMDkyMyAxMiA0MS42NjYgMTIuNTM1NiA0MC40MDU4IDEzLjgzOThDNDAuMTM3NyAxMi4yMzE5IDM5LjI0NzYgMTEuMjcyIDM3Ljg5MjYgMTAuNjU1OEMzNy4xODM2IDEwLjMzNTkgMzYuNDY2OCAxMC4wMTU2IDM1Ljk3MDIgOS4zMTk4MkMzNS42MjM1IDguODIzNzMgMzUuNTI5MyA4LjI3MTk3IDM1LjM1NiA3LjcyNzU0QzM1LjI0NTYgNy4zOTk5IDM1LjEzNTMgNy4wNjM5NiAzNC43NjUxIDcuMDA3ODFDMzQuMzYzMyA2Ljk0Mzg1IDM0LjIwNTYgNy4yODc2IDM0LjA0NzkgNy41NzU2OEMzMy40MTggOC43NTE5NSAzMy4xNzMzIDEwLjA0NzkgMzMuMTk3MyAxMS4zNTk5QzMzLjI1MjQgMTQuMzEyIDM0LjQ3MzYgMTYuNjY0MSAzNi44OTk5IDE4LjMzNTlDMzcuMTc1OCAxOC41Mjc4IDM3LjI0NjYgMTguNzE5NyAzNy4xNTk3IDE5QzM2Ljk5NDYgMTkuNTc1NyAzNi43OTc0IDIwLjEzNTcgMzYuNjI0IDIwLjcxMTlDMzYuNTEzNyAyMS4wODAxIDM2LjM0ODYgMjEuMTU5NyAzNS45NjI0IDIxQzM0LjYzMDkgMjAuNDMyMSAzMy40ODEgMTkuNTkxOCAzMi40NjQ0IDE4LjU3NTdDMzAuNzM5MyAxNi44NzIxIDI5LjE3OTIgMTQuOTkxNyAyNy4yMzM0IDEzLjUyQzI2Ljc3NjQgMTMuMTc1OCAyNi4zMTkzIDEyLjg1NiAyNS44NDY3IDEyLjU1MThDMjMuODYxOCAxMC41ODQgMjYuMTA2OSA4Ljk2Nzc3IDI2LjYyNyA4Ljc3NTg4QzI3LjE3MDQgOC41NzU2OCAyNi44MTU5IDcuODg3NyAyNS4wNTkxIDcuODk2QzIzLjMwMjIgNy45MDM4MSAyMS42OTUzIDguNTAzOTEgMTkuNjQ3IDkuMzAzNzFDMTkuMzQ3NyA5LjQyMzgzIDE5LjAzMjIgOS41MTE3MiAxOC43MDk1IDkuNTgzOThDMTYuODUwMSA5LjIyMzYzIDE0LjkxOTkgOS4xNDM1NSAxMi45MDMzIDkuMzc1OThDOS4xMDU5NiA5LjgwNzYyIDYuMDcyNzUgMTEuNjM5NiAzLjg0MzI2IDE0Ljc2ODFDMS4xNjQ1NSAxOC41Mjc4IDAuNTM0MTggMjIuNzk5OCAxLjMwNjY0IDI3LjI1NTlDMi4xMTc2OCAzMS45NTIxIDQuNDY1ODIgMzUuODM5OCA4LjA3MzczIDM4Ljg3OTlDMTEuODE1OSA0Mi4wMzIyIDE2LjEyNTUgNDMuNTc2MiAyMS4wNDEgNDMuMjgwM0MyNC4wMjY5IDQzLjEwNCAyNy4zNTE2IDQyLjY5NjMgMzEuMTAxNiAzOS40NTYxQzMyLjA0NjkgMzkuOTM2IDMzLjAzOTYgNDAuMTI3OSAzNC42ODYgNDAuMjcyQzM1Ljk1NDYgNDAuMzkyMSAzNy4xNzU4IDQwLjIwOCAzOC4xMjExIDQwLjAwNzhDMzkuNjAyMSAzOS42ODggMzkuNDk5NSAzOC4yODgxIDM4Ljk2MzkgMzguMDMyMkMzNC42MjMgMzUuOTY3OCAzNS41NzYyIDM2LjgwODEgMzQuNzEgMzYuMTI3OUMzNi45MTU1IDMzLjQ2MzkgNDAuMjQwMiAzMC42OTU4IDQxLjU0IDIxLjcyOEM0MS42NDI2IDIxLjAxNjEgNDEuNTU1NyAyMC41Njc5IDQxLjU0IDE5Ljk5MTdDNDEuNTMyMiAxOS42Mzk2IDQxLjYxMDggMTkuNTAzOSA0Mi4wMDQ5IDE5LjQ2MzlDNDMuMDkyMyAxOS4zMzU5IDQ0LjE0NzkgMTkuMDMxNyA0NS4xMTY3IDE4LjQ4NzhDNDcuOTI5MiAxNi45MTk5IDQ5LjA2NCAxNC4zNDM4IDQ5LjMzMTUgMTEuMjU1OUM0OS4zNzExIDEwLjc4MzcgNDkuMzIzNyAxMC4yOTU5IDQ4LjgzNTQgMTAuMDQ3OVpNMjQuMzI2MiAzNy44Mzk4QzIwLjExOTYgMzQuNDYzOSAxOC4wNzkxIDMzLjM1MjEgMTcuMjM1OCAzMy4zOTk5QzE2LjQ0ODIgMzMuNDQ4MiAxNi41ODk4IDM0LjM2ODIgMTYuNzYzMiAzNC45Njc4QzE2Ljk0NDMgMzUuNTYwMSAxNy4xODEyIDM1Ljk2ODMgMTcuNTExNyAzNi40ODc4QzE3Ljc0MDIgMzYuODMyIDE3Ljg5NzkgMzcuMzQ0MiAxNy4yODMyIDM3LjcyOEMxNS45MjgyIDM4LjU4NCAxMy41NzI4IDM3LjQzOTkgMTMuNDYyNCAzNy4zODM4QzEwLjcyMDcgMzUuNzM1OCA4LjQyODIyIDMzLjU2MDEgNi44MTM0OCAzMC41ODRDNS4yNTM0MiAyNy43MTk3IDQuMzQ3NjYgMjQuNjQ3OSA0LjE5Nzc1IDIxLjM2NzdDNC4xNTgyIDIwLjU3NTcgNC4zODY3MiAyMC4yOTU5IDUuMTU4NjkgMjAuMTUxOUM2LjE3NTI5IDE5Ljk2IDcuMjIzMTQgMTkuOTE5OSA4LjIzOTI2IDIwLjA3MThDMTIuNTMyNyAyMC43MTE5IDE2LjE4ODUgMjIuNjcxOSAxOS4yNTI5IDI1Ljc3NTlDMjEuMDAyIDI3LjU0MzkgMjIuMzI1MiAyOS42NTU4IDIzLjY4ODUgMzEuNzIwMkMyNS4xMzc3IDMzLjkxMjEgMjYuNjk3OCAzNiAyOC42ODMxIDM3LjcxMTlDMjkuMzg0MyAzOC4zMTIgMjkuOTQzNCAzOC43NjgxIDMwLjQ3OSAzOS4xMDRDMjguODY0MyAzOS4yODgxIDI2LjE2OTkgMzkuMzI4MSAyNC4zMjYyIDM3LjgzOThaTTI2LjM0MzMgMjQuNjAwMUMyNi4zNDMzIDI0LjI0OCAyNi42MTkxIDIzLjk2NzggMjYuOTY1OCAyMy45Njc4QzI3LjA0NDQgMjMuOTY3OCAyNy4xMTUyIDIzLjk4MzkgMjcuMTc4MiAyNC4wMDc4QzI3LjI2NTEgMjQuMDQgMjcuMzQzOCAyNC4wODc5IDI3LjQwNjcgMjQuMTYwMkMyNy41MTcxIDI0LjI3MiAyNy41ODAxIDI0LjQzMjEgMjcuNTgwMSAyNC42MDAxQzI3LjU4MDEgMjQuOTUyMSAyNy4zMDQyIDI1LjIzMTkgMjYuOTU3NSAyNS4yMzE5QzI2LjYxMDggMjUuMjMxOSAyNi4zNDMzIDI0Ljk1MjEgMjYuMzQzMyAyNC42MDAxWk0zMi42MDY0IDI3Ljg3OTlDMzIuMjA0NiAyOC4wNDc5IDMxLjgwMjcgMjguMTkxOSAzMS40MTY1IDI4LjIwOEMzMC44MTc5IDI4LjIzOTcgMzAuMTY0MSAyNy45OTIyIDI5LjgwOTYgMjcuNjg4QzI5LjI1ODMgMjcuMjE1OCAyOC44NjQzIDI2Ljk1MjEgMjguNjk4NyAyNi4xMjc5QzI4LjYyNzkgMjUuNzc1OSAyOC42Njc1IDI1LjIzMTkgMjguNzMwNSAyNC45MTk5QzI4Ljg3MjEgMjQuMjQ4IDI4LjcxNDQgMjMuODE1OSAyOC4yNDk1IDIzLjQyMzhDMjcuODcxNiAyMy4xMDQgMjcuMzkxMSAyMy4wMTYxIDI2Ljg2MzMgMjMuMDE2MUMyNi42NjYgMjMuMDE2MSAyNi40ODQ5IDIyLjkyNzcgMjYuMzUxMSAyMi44NTZDMjYuMTMwNCAyMi43NDQxIDI1Ljk0OTIgMjIuNDYzOSAyNi4xMjI2IDIyLjEyMDFDMjYuMTc3NyAyMi4wMDc4IDI2LjQ0NTggMjEuNzM1OCAyNi41MDg4IDIxLjY4OEMyNy4yMjU2IDIxLjI3MiAyOC4wNTI3IDIxLjQwNzcgMjguODE2OSAyMS43MTk3QzI5LjUyNTkgMjIuMDE2MSAzMC4wNjE1IDIyLjU2MDEgMzAuODM0IDIzLjMyODFDMzEuNjIxNiAyNC4yNTU5IDMxLjc2MzIgMjQuNTExNyAzMi4yMTI0IDI1LjIwOEMzMi41NjY5IDI1Ljc1MiAzMi44OTAxIDI2LjMxMiAzMy4xMTA0IDI2Ljk1MjFDMzMuMjQ0NiAyNy4zNTIxIDMzLjA3MTMgMjcuNjgwMiAzMi42MDY0IDI3Ljg3OTlaIiBmaWxsPSIjZmZmZmZmIi8+PC9zdmc+" alt="DSH"></span>' +
      '<span class="pwv-title">dsh</span>' +
      '<span class="pwv-author">@ Mr.chen</span>' +
      '</div>' +
      '<div class="pwv-btns">' +
      '<button class="pwv-btn pwv-theme" title="切换深色/浅色主题">' +
      '<svg viewBox="0 0 16 16"><path d="M13 9.3A5.5 5.5 0 1 1 6.7 3a4.4 4.4 0 0 0 6.3 6.3z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg></button>' +
      '<span class="pwv-sep"></span>' +
      '<button class="pwv-btn pwv-zoomout" title="缩小">' +
      '<svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.6 10.6 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M5.2 7h3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></button>' +
      '<span class="pwv-zoompct">100%</span>' +
      '<button class="pwv-btn pwv-zoomin" title="放大">' +
      '<svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.6 10.6 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M7 5.2v3.6M5.2 7h3.6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg></button>' +
      '<button class="pwv-btn pwv-zoomreset" title="重置为 100%">' +
      '<svg viewBox="0 0 16 16"><path d="M13 8a5 5 0 1 1-1.4-3.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M13 1.8v3.2H9.8" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
      '<span class="pwv-sep"></span>' +
      '<button class="pwv-btn pwv-min" title="最小化">' +
      '<svg viewBox="0 0 16 16"><path d="M3 8h10" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>' +
      '<button class="pwv-btn pwv-max" title="最大化">' +
      '<svg viewBox="0 0 16 16"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></button>' +
      '<button class="pwv-btn pwv-close" title="关闭">' +
      '<svg viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button>' +
      '</div>';
    document.body.appendChild(tb);
    document.documentElement.classList.add('pwv-shifted');

    var api = getApi();
    function ctl(a) { if (api && api.windowControl) api.windowControl(a); }
    var maxed = false;
    function refreshMax() {
      tb.querySelector('.pwv-max').innerHTML = maxed
        ? '<svg viewBox="0 0 16 16"><rect x="3.5" y="5.5" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M6.5 3.5H12a.5.5 0 0 1 .5.5v5.5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'
        : '<svg viewBox="0 0 16 16"><rect x="3.5" y="3.5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';
      tb.querySelector('.pwv-max').title = maxed ? '还原' : '最大化';
    }
    function toggleMax() {
      maxed = !maxed;
      ctl(maxed ? 'max' : 'restore');
      refreshMax();
    }
    tb.querySelector('.pwv-min').addEventListener('click', function () { ctl('min'); });
    tb.querySelector('.pwv-max').addEventListener('click', toggleMax);
    tb.querySelector('.pwv-close').addEventListener('click', function () { ctl('close'); });
    tb.querySelector('.pwv-left').addEventListener('dblclick', toggleMax);
    // 自绘窗口拖拽(替换 pywebview 内置: 修复缩放后拖动错位/顿挫)
    tb.querySelector('.pwv-left').addEventListener('mousedown', function (ev) {
      if (ev.button !== 0) return;
      ev.preventDefault();
      ev.stopPropagation();
      var dpr = window.devicePixelRatio || 1;
      var sx = ev.screenX, sy = ev.screenY;
      var wx = window.screenX, wy = window.screenY;
      function move(ev2) {
        var nx = Math.round(wx + (ev2.screenX - sx) / dpr);
        var ny = Math.round(wy + (ev2.screenY - sy) / dpr);
        var a = getApi();
        if (a && a.moveWindowTo) a.moveWindowTo(nx, ny);
      }
      function up() {
        window.removeEventListener('mousemove', move);
        window.removeEventListener('mouseup', up);
      }
      window.addEventListener('mousemove', move);
      window.addEventListener('mouseup', up);
    });

    // 缩放控件(类似浏览器缩放; 内容区缩放, 标题栏不缩放)
    window.setZoomPct = function (p) {
      var el = document.getElementById('pwv-titlebar');
      if (el) {
        var t = el.querySelector('.pwv-zoompct');
        if (t) t.textContent = Math.round(p) + '%';
      }
    };
    window.applyZoom = function (z) {
      z = Math.max(0.5, Math.min(2, z));
      var kids = document.body.children;
      for (var i = 0; i < kids.length; i++) {
        var el = kids[i];
        if (el.id === 'pwv-titlebar' || el.classList.contains('pwv-rz') ||
            el.classList.contains('pwv-pet') || el.classList.contains('pwv-petpanel')) continue;
        el.style.zoom = (Math.abs(z - 1) < 0.001) ? '' : z;
      }
      document.body.style.overflow = (Math.abs(z - 1) < 0.001) ? '' : 'hidden';
      window.setZoomPct(Math.round(z * 100));
    };
    tb.querySelector('.pwv-zoomout').addEventListener('click', function () {
      var a = getApi(); if (a && a.zoomBy) a.zoomBy(-0.1);
    });
    tb.querySelector('.pwv-zoomin').addEventListener('click', function () {
      var a = getApi(); if (a && a.zoomBy) a.zoomBy(0.1);
    });
    tb.querySelector('.pwv-zoomreset').addEventListener('click', function () {
      var a = getApi(); if (a && a.zoomReset) a.zoomReset();
    });

    // 主题快捷切换: 直接改写 ~/.dsh/settings.yaml 的 ui-theme.preference,
    // DSH 的 settings-file 监听器(热重载)会广播给界面实时应用 —— 不再模拟点击
    // 设置面板, 不受 DSH 界面结构/类名变化影响。
    function _currentDshTheme() {
      try {
        var cs = (getComputedStyle(document.documentElement).colorScheme || '').toLowerCase();
        if (cs === 'dark' || cs === 'light') return cs;
      } catch (e) {}
      // 兜底: 用标题栏实际背景亮度判断(跟随主题的 --dsw 变量)
      try {
        var tbEl = document.getElementById('pwv-titlebar');
        if (tbEl) {
          var bg = getComputedStyle(tbEl).backgroundColor || '';
          var m = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
          if (m) {
            var lum = (+m[1] * 299 + +m[2] * 587 + +m[3] * 114) / 1000;
            return lum < 128 ? 'dark' : 'light';
          }
        }
      } catch (e) {}
      return null;
    }
    // 主题按钮图标随主题变化: 深色 -> 白色月亮, 浅色 -> 红色太阳
    function updateThemeIcon() {
      var btn = tb.querySelector('.pwv-theme');
      if (!btn) return;
      var cur = _currentDshTheme();
      if (cur === 'light') {
        btn.innerHTML = '<svg viewBox="0 0 16 16" style="color:#f43f5e">' +
          '<circle cx="8" cy="8" r="3.1" fill="currentColor"/>' +
          '<path d="M8 1.3v1.9M8 12.8v1.9M1.3 8h1.9M12.8 8h1.9M3.2 3.2l1.35 1.35M11.45 11.45l1.35 1.35M12.8 3.2l-1.35 1.35M4.55 11.45l-1.35 1.35" ' +
          'stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
      } else {
        btn.innerHTML = '<svg viewBox="0 0 16 16" style="color:#ffffff">' +
          '<path d="M13.2 9.4A5.6 5.6 0 1 1 6.6 2.8a4.5 4.5 0 0 0 6.6 6.6z" fill="currentColor"/></svg>';
      }
    }
    updateThemeIcon();
    // 轮询兜底(覆盖在设置面板手动切主题/外部改设置的情况)
    setInterval(updateThemeIcon, 800);
    tb.querySelector('.pwv-theme').addEventListener('click', function () {
      var cur = _currentDshTheme();
      if (!cur) return;
      var a = getApi();
      if (a && a.setTheme) {
        a.setTheme(cur === 'dark' ? 'light' : 'dark');
      }
      // 主题由 DSH 热重载应用(约 100~300ms), 分级延时刷新图标
      updateThemeIcon();
      setTimeout(updateThemeIcon, 250);
      setTimeout(updateThemeIcon, 600);
      setTimeout(updateThemeIcon, 1200);
    });

    // ---- 右下角宠物挂件(DeepSeek 账户信息; 随应用存在, 换机重装也有) ----
    var pet = document.createElement('div');
    pet.className = 'pwv-pet';
    pet.title = 'DeepSeek 账户';
    var logoImg = tb.querySelector('.pwv-logo img');
    pet.innerHTML = '<img src="' + (logoImg ? logoImg.src : '') + '" alt="pet">';
    document.body.appendChild(pet);

    var panel = document.createElement('div');
    panel.className = 'pwv-petpanel';
    panel.innerHTML =
      '<div class="pwv-ph"><span>DeepSeek 账户</span><button class="pwv-pc">\u2715</button></div>' +
      '<div class="pwv-row" title="账户余额(DeepSeek 官方接口实时查询)"><span>账户余额</span><span id="pwv-balance">加载中…</span></div>' +
      '<div class="pwv-row" title="今日 Token(来自本机 DSH 会话日志, 含推理 token)">' +
      '<span>今日 Token</span><span id="pwv-today-tokens" class="pwv-num">加载中…</span></div>' +
      '<div class="pwv-row" title="今日消费(按 DeepSeek 官方价目本地估算≈, 实际以官网账单为准)">' +
      '<span>今日消费</span><span id="pwv-today-cost" class="pwv-num">加载中…</span></div>' +
      '<div class="pwv-row" title="今日请求(来自本机 DSH 会话日志)">' +
      '<span>今日请求</span><span id="pwv-today-req" class="pwv-num">加载中…</span></div>' +
      '<div class="pwv-note">今日Token/消费/请求由本机DSH会话日志统计，可能和官网存在出入，详细信息点击下方官网查看！</div>' +
      '<div class="pwv-pbtns">' +
      '<button class="pwv-pbtn" id="pwv-refresh">刷新</button>' +
      '<button class="pwv-pbtn pwv-link" id="pwv-site">官网 \u2197</button>' +
      '</div>';
    document.body.appendChild(panel);

    function balEl() { return document.getElementById('pwv-balance'); }
    function renderBalance(r) {
      var el = balEl(); if (!el) return;
      if (!r || !r.ok) {
        var e = r && r.error;
        el.innerHTML = e === 'no_key' ? '未配置 API Key' :
          (e === 'key_invalid' ? 'Key 无效' :
          (e === 'insufficient' ? '余额不足' : ('获取失败 ' + (e || ''))));
        return;
      }
      var infos = r.data && r.data.balance_infos;
      if (infos && infos.length) {
        var i = infos[0];
        el.innerHTML = '\u00A5 ' + i.total_balance +
          '<div class="pwv-sub">充值 ' + i.topped_up_balance + ' \u00B7 赠送 ' + i.granted_balance + '</div>';
      } else {
        el.innerHTML = '暂无余额信息';
      }
    }
    function refreshBalance() {
      var el = balEl(); if (el) el.innerHTML = '加载中…';
      var a = getApi();
      if (a && a.getBalance) a.getBalance().then(renderBalance);
    }
    function fmtTokens(n) {
      n = Math.round(Number(n) || 0);
      return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
    // Token 显示: 保留千分位原值, 括号内附加单位(≥1亿 用亿, ≥1万 用万, 万以下不加)
    function fmtTokensUnit(n) {
      n = Math.round(Number(n) || 0);
      var s = fmtTokens(n);
      var u = '';
      if (n >= 1e8 || n >= 9999500) {          // 万位四舍五入后 ≥10000 万 -> 直接用亿
        u = trimUnit((n / 1e8).toFixed(2)) + '亿';
      } else if (n >= 1e4) {
        u = trimUnit((n / 1e4).toFixed(2)) + '万';
      }
      return u ? s + ' (' + u + ')' : s;
    }
    function trimUnit(x) {
      return String(x).replace(/0+$/, '').replace(/\.$/, '');
    }
    function fmtMoney(x) {
      var v = (Number(x) || 0).toFixed(2);
      var neg = v.charAt(0) === '-';
      if (neg) v = v.slice(1);
      var parts = v.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return '\u2248 ' + (neg ? '-' : '') + '\u00A5' + parts.join('.');
    }
    function fmtReq(n) {
      return fmtTokens(n) + ' 次';
    }
    var USAGE_FIELDS = [
      ['pwv-today-tokens', 'today', 'tokens',   fmtTokensUnit],
      ['pwv-today-cost',   'today', 'cost',     fmtMoney],
      ['pwv-today-req',    'today', 'requests', fmtReq]
    ];
    function renderUsage(r) {
      // 拿不到就不展示: 接口失败/不可用(如 404)时整组隐藏, 不显示错误文案
      if (!r || !r.ok) {
        for (var j = 0; j < USAGE_FIELDS.length; j++) {
          var elj = document.getElementById(USAGE_FIELDS[j][0]);
          if (!elj) continue;
          var rowj = elj.closest('.pwv-row');
          if (rowj) rowj.style.display = 'none';
        }
        return;
      }
      for (var i = 0; i < USAGE_FIELDS.length; i++) {
        var el = document.getElementById(USAGE_FIELDS[i][0]);
        if (!el) continue;
        var row = el.closest('.pwv-row');
        var seg = r.data[USAGE_FIELDS[i][1]] || {};
        var v = seg[USAGE_FIELDS[i][2]];
        if (v === undefined || v === null) {
          // 官方接口未返回该字段 -> 不展示这一行(拿不到就不展示)
          if (row) row.style.display = 'none';
          continue;
        }
        if (row) row.style.display = '';
        el.textContent = USAGE_FIELDS[i][3](v);
      }
    }
    function refreshUsage() {
      for (var i = 0; i < USAGE_FIELDS.length; i++) {
        var el = document.getElementById(USAGE_FIELDS[i][0]);
        if (el) el.textContent = '加载中…';
      }
      var a = getApi();
      if (a && a.getUsage) a.getUsage().then(renderUsage);
    }
    function openPanel() {
      refreshBalance();
      refreshUsage();
      panel.classList.add('show');
    }
    pet.addEventListener('click', function () {
      if (panel.classList.contains('show')) { panel.classList.remove('show'); return; }
      openPanel();
    });
    panel.querySelector('.pwv-pc').addEventListener('click', function () {
      panel.classList.remove('show');
    });
    panel.querySelector('#pwv-refresh').addEventListener('click', function () {
      refreshBalance();
      refreshUsage();
    });
    panel.querySelector('#pwv-site').addEventListener('click', function () {
      var a = getApi();
      if (a && a.openDeepSeekSite) a.openDeepSeekSite();
    });
    // 点击面板/宠物之外的任意区域时自动关闭面板(捕获阶段监听,
    // 避免被页面内其它元素 stopPropagation 拦截; 面板内按钮/宠物自身的点击不受影响)
    document.addEventListener('click', function (ev) {
      if (panel.classList.contains('show') &&
          !panel.contains(ev.target) && !pet.contains(ev.target)) {
        panel.classList.remove('show');
      }
    }, true);

    // 无边框窗口拖拽缩放(边缘/四角手柄)
    var RZ_CFG = { n:{w:0,h:-1}, s:{w:0,h:1}, e:{w:1,h:0}, w:{w:-1,h:0},
                   ne:{w:1,h:-1}, nw:{w:-1,h:-1}, se:{w:1,h:1}, sw:{w:-1,h:1} };
    ['n','s','e','w','ne','nw','se','sw'].forEach(function (edge) {
      var el = document.createElement('div');
      el.className = 'pwv-rz pwv-rz-' + edge;
      document.body.appendChild(el);
      el.addEventListener('pointerdown', function (ev) {
        ev.preventDefault();
        el.setPointerCapture(ev.pointerId);
        var c = RZ_CFG[edge];
        var dpr = window.devicePixelRatio || 1;
        var sx = ev.screenX, sy = ev.screenY;
        var sw0 = window.innerWidth, sh0 = window.innerHeight;
        function move(ev2) {
          if (maxed) return;
          var nw = Math.max(1024, sw0 + c.w * (ev2.screenX - sx) / dpr);
          var nh = Math.max(618,  sh0 + c.h * (ev2.screenY - sy) / dpr);
          var a2 = getApi();
          if (a2 && a2.resizeWindow) a2.resizeWindow(nw, nh, edge);
        }
        function up() {
          try { el.releasePointerCapture(ev.pointerId); } catch (e) {}
          el.removeEventListener('pointermove', move);
          el.removeEventListener('pointerup', up);
        }
        el.addEventListener('pointermove', move);
        el.addEventListener('pointerup', up);
      });
    });
  } catch (e) {}
})();
'''


# 消除跳转白闪的文档创建脚本(经 AddScriptToExecuteOnDocumentCreatedAsync 注入):
# 文档创建瞬间 documentElement 尚不存在, 先轮询等待; 注入
# html,body 深色背景(!important); 等 DSH 主题变量 --dsw-alias-bg-base
# 连续 3 次稳定(约 0.5s)后再移除覆盖, 避免主题浅色过渡期误移除导致白闪,
# 8 秒兜底移除。对所有后续导航生效(含安装页, 安装页本身是深色, 无影响)。
NOFLASH_SCRIPT = (
    "try{var iv=setInterval(function(){"
    "var root=document.documentElement;"
    "if(!root)return;clearInterval(iv);"
    "try{var s=document.createElement('style');"
    "s.id='pwv-noflash';"
    "s.textContent='html,body{background:#0b1220 !important;}';"
    "(document.head||root).appendChild(s);"
    "var last='',cnt=0;"
    "var iv2=setInterval(function(){"
    "var v=(getComputedStyle(document.documentElement)"
    ".getPropertyValue('--dsw-alias-bg-base')||'').trim();"
    "if(v&&v!=='transparent'){"
    "if(v===last){cnt++;}else{cnt=0;last=v;}"
    "if(cnt>=3){clearInterval(iv2);"
    "try{s.parentNode&&s.parentNode.removeChild(s);}catch(e){}}"
    "}else{cnt=0;last='';}"
    "},150);"
    "setTimeout(function(){clearInterval(iv2);"
    "try{s.parentNode&&s.parentNode.removeChild(s);}catch(e){}},8000);"
    "}catch(e){}"
    "},10);"
    "setTimeout(function(){clearInterval(iv);},3000);"
    "}catch(e){}"
)
