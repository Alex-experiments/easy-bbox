"""Test file for bbox/utils.py"""

import unittest

from easy_bbox import Bbox, nms


class TestNMS(unittest.TestCase):
    """Unit tests for the nms function."""

    def test_nms_empty_input(self):
        """Test that the NMS function returns an empty list when the input is empty."""
        self.assertEqual(nms([], []), [])

    def test_nms_single_bbox(self):
        """Test that the NMS function returns the single bbox when there is only one bbox."""
        bboxes = [Bbox(0, 0, 10, 10)]
        scores = [0.9]
        self.assertEqual(nms(bboxes, scores), [(Bbox(0, 0, 10, 10), 0.9)])

    def test_nms_no_suppression(self):
        """Test that the NMS function returns all bboxes when there is no suppression."""
        bboxes = [Bbox(0, 0, 10, 10), Bbox(20, 20, 30, 30)]
        scores = [0.9, 0.8]
        self.assertEqual(
            nms(bboxes, scores),
            [(Bbox(0, 0, 10, 10), 0.9), (Bbox(20, 20, 30, 30), 0.8)],
        )

    def test_nms_suppression(self):
        """Test that the NMS function suppresses bboxes with IoU above the threshold."""
        bboxes = [Bbox(0, 0, 10, 10), Bbox(5, 5, 15, 15)]
        scores = [0.7, 0.8]
        self.assertListEqual(
            nms(bboxes, scores, iou_threshold=0.1), [(Bbox(5, 5, 15, 15), 0.8)]
        )

        # Assert that results are ordered by decreasing score
        self.assertListEqual(
            nms(bboxes, scores, iou_threshold=1),
            sorted(zip(bboxes, scores), key=lambda x: x[1], reverse=True),
        )

    def test_nms_invalid_input(self):
        """Test that the NMS function raises a ValueError when the input is invalid."""
        bboxes = [Bbox(0, 0, 10, 10)]
        scores = [0.9, 0.8]
        with self.assertRaises(ValueError):
            nms(bboxes, scores)


if __name__ == "__main__":
    unittest.main()
