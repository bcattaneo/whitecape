// ==UserScript==
// @name            Whitecape
// @description     A proof of concept of a chess helper
// @version         1.0
// @namespace       bcattaneo.Whitecape
// @grant           none
// @include         https://lichess.org/*
// @updateURL       https://www.cattaneo.uy/whitecape/whitecape.meta.js
// @downloadURL     https://www.cattaneo.uy/whitecape/whitecape.user.js
// @icon            data:image/gif;base64,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
// ==/UserScript==
