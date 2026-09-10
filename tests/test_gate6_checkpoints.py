import unittest

from scripts.validate_gate6 import checkpoint_for_total


class Gate6CheckpointTests(unittest.TestCase):
    def test_valid_sizes(self):
        for total, checkpoint in ((100, 1), (150, 2), (200, 3), (250, 4), (500, 9)):
            self.assertEqual(checkpoint_for_total(total), checkpoint)

    def test_intermediate_size_rejected(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_GATE6_CHECKPOINT_SIZE'):
            checkpoint_for_total(225)

    def test_overflow_size_rejected(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_GATE6_CHECKPOINT_SIZE'):
            checkpoint_for_total(501)
