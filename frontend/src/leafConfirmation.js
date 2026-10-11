export const LEAF_CONFIRMATION_ERROR =
  "Confirm that the image's main subject is a crop leaf before analysis.";

export function getLeafConfirmationError(isConfirmed) {
  return isConfirmed ? "" : LEAF_CONFIRMATION_ERROR;
}
