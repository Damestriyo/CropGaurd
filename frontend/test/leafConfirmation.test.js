import assert from "node:assert/strict";
import test from "node:test";

import {
  getLeafConfirmationError,
  LEAF_CONFIRMATION_ERROR,
} from "../src/leafConfirmation.js";

test("prevents analysis until the user confirms the image shows a crop leaf", () => {
  assert.equal(getLeafConfirmationError(false), LEAF_CONFIRMATION_ERROR);
  assert.equal(getLeafConfirmationError(true), "");
});
