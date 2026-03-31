#!/usr/bin/env node
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const target = pathToFileURL(path.resolve(__dirname, "../../../lib/web-fetch-md/dist/fetchmd.js")).href;
import(target);
