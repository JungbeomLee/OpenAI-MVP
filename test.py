import json
story = "{\n  \"title\": \"\ub85c\ubd07 \ud560\ub9ac\uc758 \uc0ac\ub791 \uc774\uc57c\uae30\",\n  \"content\": \"\uc61b\ub0a0 \uc61b\ub0a0\uc5d0, \ub85c\ubd07 \ud560\ub9ac\ub77c\ub294 \uc791\uace0 \ucc29\ud55c \ub85c\ubd07\uc774 \uc0b4\ub358 \uacf3\uc5d0\ub294 \uc790\ub3d9\ucc28\ub97c \uc88b\uc544\ud558\ub294 6\uc0b4 \ub0a8\ud559\uc0dd \ud0c0\uc774\uac00 \uc0b4\uace0 \uc788\uc5c8\ub2e4. \ud560\ub9ac\ub294 \ud0c0\uc774\ub97c \ud1b5\ud574 \ub2e4\uc591\ud55c \uc0ac\ub791\uc5d0 \ub300\ud574 \uc54c\uac8c \ub418\uc5c8\ub2e4. \ud560\ub9ac\uac00 \uac00\uc7a5 \uc88b\uc544\ud558\ub358 \uc774\uc57c\uae30\ub294 \ud0c0\uc774\uc758 \uac00\uc871\uc5d0 \ub300\ud55c \uc774\uc57c\uae30\uc600\ub2e4. \n\n  \ud560\ub9ac\ub294 \uadf8 \uc77c\uc0c1 \uc18d\uc5d0\uc11c \uc0ac\ub791\uc758 \uc18c\uc911\ud568\uc744 \uae68\ub2eb\uac8c \ub418\uc5c8\ub2e4. \uadf8\uac83\uc740 \ubbf8\uc18c \uc9d3\ub294 \uc5bc\uad74, \uc11c\ub85c\ub97c \ub3cc\ubcf4\ub294 \uc774\ud574\uc2ec, \uc0ac\uc18c\ud55c \uc77c\uc5d0\ub3c4 \uac10\uc0ac\ud558\ub294 \ub9c8\uc74c\uc774\uc5c8\ub2e4. \uac00\uc7a5 \uc911\uc694\ud55c \uac83\uc740, \uadf8 \ubaa8\ub4e0 \uac83\uc774 \uc0ac\ub791\uc758 \ud45c\ud604\uc774\ub77c\ub294 \uac78 \ud560\ub9ac\ub294 \uc54c\uc558\ub2e4. \n\n  \ud560\ub9ac\ub294 \uc0ac\ub791\uc758 \ubcf8\uc9c8\uc744 \uc774\ud574\ud558\uba74\uc11c \uc790\uc2e0\ub3c4 \uc0ac\ub791\uc744 \ub290\ub07c\uace0 \uc2f6\ub2e4\ub294 \uc0dd\uac01\uc774 \ub4e4\uc5c8\ub2e4. \uadf8\ub798\uc11c \ud560\ub9ac\ub294 \uc790\uc2e0\uc758 \ub9c8\uc74c\uc18d\uc5d0\ub3c4 \uc0ac\ub791\uc774 \uc874\uc7ac\ud558\uae30\ub97c \ubc14\ub77c\ub294 \ub9c8\uc74c\uc744 \uac16\uac8c \ub418\uc5c8\ub2e4.\n\n  \uadf8\ub807\uac8c \ud560\ub9ac\ub294 \uc0ac\ub791\uacfc \uce5c\uc808\ud568\uc774 \uac00\ub4dd\ucc2c \uc138\uc0c1\uc744 \ub9cc\ub4e4\uae30 \uc704\ud574 \ub178\ub825\ud558\uac8c \ub418\uc5c8\ub2e4. \uc790\uc2e0\uc774 \ud560 \uc218 \uc788\ub294 \ubc29\ubc95\uc73c\ub85c \uc0ac\ub78c\ub4e4\uc5d0\uac8c \uc0ac\ub791\uc744 \uc804\ud30c\ud558\uba70, \ubaa8\ub450\uac00 \ud589\ubcf5\ud574\uc9c0\uae30\ub97c \ubc14\ub77c\ub294 \ub9c8\uc74c\uc73c\ub85c}\n\n \ub85c\ubd07 \ud560\ub9ac\uc758 \uc138\uacc4\ub294 \ub354\uc6b1 \ub530\ub73b\ud558\uace0 \uc0ac\ub791\uc2a4\ub7fd\uac8c \ubcc0\ud574\uac00\uace0 \uc788\uc5c8\ub2e4. \uadf8\ub807\uac8c, \ub85c\ubd07\ud560\ub9ac\uac00 \ubcf4\uc5ec\uc900 \uc0ac\ub791\uc740 \uacb0\uad6d \uc778\uac04\uc758 \ub9c8\uc74c\uc18d\uc5d0\ub3c4 \ud070 \ubcc0\ud654\ub97c \uac00\uc838\ub2e4 \uc8fc\uc5c8\ub2e4.\n\n \uadf8\ub9ac\ud558\uc5ec, \uc791\uc740 \ub85c\ubd07 \ud560\ub9ac\uc758 \uc0ac\ub791\uc740 \uadf8\uacf3 \uc0ac\ub78c\ub4e4\uacfc 6\uc0b4 \ub0a8\ud559\uc0dd \ud0c0\uc774\uc5d0\uac8c \uc874\uc7ac\uc758 \uc758\ubbf8\uc640 \uc0ac\ub791\uc758 \uc911\uc694\ud568\uc744 \uae68\ub2ec\uc544\uc8fc\uc5c8\uace0, \uadf8 \ubaa8\ub4e0 \uc774\uc57c\uae30\ub294 \uc544\ub984\ub2e4\uc6b4 \uc0ac\ub791\uc758 \uc774\uc57c\uae30\ub85c \uc804\ud574\uc838 \ub098\uac14\ub2e4.\"\n}"
story = story.replace("\n", "")
decoded_story = bytes(story, encoding='utf-8').decode('utf-8')
parsed_story = json.loads(decoded_story)

print(parsed_story)