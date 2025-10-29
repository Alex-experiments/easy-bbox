import unittest

from easy_bbox import Bbox


class TestBbox(unittest.TestCase):
    """Unit tests for the Bbox class."""

    def setUp(self):
        self.bbox = Bbox(10, 20, 30, 40)

    def test_initialization(self):
        """Test Bbox initialization with left, top, right, and bottom coordinates."""
        self.assertEqual(self.bbox.left, 10)
        self.assertEqual(self.bbox.top, 20)
        self.assertEqual(self.bbox.right, 30)
        self.assertEqual(self.bbox.bottom, 40)

        # Test invalid bbox initialization
        with self.assertRaises(ValueError):
            Bbox(10, 0, 0, 10)

        with self.assertRaises(ValueError):
            Bbox(0, 10, 10, 0)

    def test_copy(self):
        """Test Bbox copy method."""
        copied_bbox = self.bbox.copy()

        # Check that the copied instance is not the same object as the original
        self.assertIsNot(self.bbox, copied_bbox)

        # Check that the copied instance is equal to the original
        self.assertEqual(self.bbox, copied_bbox)

    # region Properties
    def test_width(self):
        """Test width property."""
        self.assertEqual(self.bbox.width, self.bbox.right - self.bbox.left)

    def test_height(self):
        """Test height property."""
        self.assertEqual(self.bbox.height, self.bbox.bottom - self.bbox.top)

    def test_area(self):
        """Test area property."""
        self.assertEqual(self.bbox.area, self.bbox.width * self.bbox.height)

    def test_center(self):
        """Test center property."""
        self.assertEqual(self.bbox.center, (20, 30))

    def test_aspect_ratio(self):
        """Test aspect ratio property."""
        self.assertEqual(self.bbox.aspect_ratio, 1)
        self.assertEqual(Bbox(-5, 0, 5, 5).aspect_ratio, 2)
        self.assertEqual(Bbox(0, -5, 5, 5).aspect_ratio, 0.5)

    # end region

    # region Dunder methods
    def test_eq(self):
        """Test Bbox equality."""
        self.assertTrue(self.bbox == Bbox(10, 20, 30, 40))
        self.assertFalse(self.bbox == Bbox(20, 30, 40, 50))

        # Test NotImplemented case
        class OtherClass:
            pass

        other_instance = OtherClass()
        self.assertEqual(self.bbox.__eq__(other_instance), NotImplemented)

    def test_repr(self):
        """Test Bbox repr."""
        self.assertEqual(repr(self.bbox), "Bbox(left=10, top=20, right=30, bottom=40)")

    def test_str(self):
        """Test Bbox string representation."""
        self.assertEqual(str(self.bbox), "Bbox(left=10, top=20, right=30, bottom=40)")

    def test_or(self):
        """Test Bbox union with or."""
        self.assertEqual(self.bbox.__or__, self.bbox.union)

    def test_and(self):
        """Test Bbox intersection with and."""
        self.assertEqual(self.bbox.__and__, self.bbox.intersection)

    # end region

    # region From
    def test_from_tlbr(self):
        """Test Bbox creation from top-left and bottom-right coordinates."""
        bbox = Bbox.from_tlbr(
            (self.bbox.left, self.bbox.top, self.bbox.right, self.bbox.bottom)
        )
        self.assertEqual(bbox, self.bbox)

        # Assert that any list that has a different length than 4 raises a ValueError
        with self.assertRaises(ValueError):
            Bbox.from_tlbr([])

        with self.assertRaises(ValueError):
            Bbox.from_tlbr((0.0,))

        with self.assertRaises(ValueError):
            Bbox.from_tlbr(range(3))

        with self.assertRaises(ValueError):
            Bbox.from_tlbr(range(5))

        # Assert that invalid bboxes raises an error
        with self.assertRaises(ValueError):
            Bbox.from_tlbr([0, 0, -10, 10])

        with self.assertRaises(ValueError):
            Bbox.from_tlbr((0, 0, 10, -10))

    def test_from_tlwh(self):
        """Test Bbox creation from top-left coordinates and width and height."""
        bbox = Bbox.from_tlwh(
            (self.bbox.left, self.bbox.top, self.bbox.width, self.bbox.height)
        )
        self.assertEqual(bbox, self.bbox)

        # Assert that any list that has a different length than 4 raises a ValueError
        with self.assertRaises(ValueError):
            Bbox.from_tlwh([])

        with self.assertRaises(ValueError):
            Bbox.from_tlwh((0.0,))

        with self.assertRaises(ValueError):
            Bbox.from_tlwh(range(3))

        with self.assertRaises(ValueError):
            Bbox.from_tlwh(range(5))

        # Assert that invalid bboxes raises an error
        with self.assertRaises(ValueError):
            Bbox.from_tlwh([0, 0, -10, 10])

        with self.assertRaises(ValueError):
            Bbox.from_tlwh((0, 0, 10, -10))

    def test_from_cwh(self):
        """Test Bbox creation from center coordinates and width and height."""
        bbox = Bbox.from_cwh((*self.bbox.center, self.bbox.width, self.bbox.height))
        self.assertEqual(bbox, self.bbox)

        # Assert that any list that has a different length than 4 raises a ValueError
        with self.assertRaises(ValueError):
            Bbox.from_cwh([])

        with self.assertRaises(ValueError):
            Bbox.from_cwh((0.0,))

        with self.assertRaises(ValueError):
            Bbox.from_cwh(range(3))

        with self.assertRaises(ValueError):
            Bbox.from_cwh(range(5))

        # Assert that invalid bboxes raises an error
        with self.assertRaises(ValueError):
            Bbox.from_cwh([0, 0, -10, 10])

        with self.assertRaises(ValueError):
            Bbox.from_cwh((0, 0, 10, -10))

    def test_from_alias_methods(self):
        """Test that alias methods are correctly set."""
        self.assertEqual(Bbox.from_xyxy, Bbox.from_tlbr)
        self.assertEqual(Bbox.from_pascal_voc, Bbox.from_tlbr)
        self.assertEqual(Bbox.from_list, Bbox.from_tlbr)
        self.assertEqual(Bbox.from_coco, Bbox.from_tlwh)

    # endregion

    # region To
    def test_to_tlbr(self):
        """Test the to_tlbr method."""
        self.assertListEqual(
            self.bbox.to_tlbr(),
            [self.bbox.left, self.bbox.top, self.bbox.right, self.bbox.bottom],
        )

    def test_to_norm_tlbr(self):
        """Test the to_norm_tlbr method."""
        self.assertListEqual(self.bbox.to_norm_tlbr(101, 101), [0.1, 0.2, 0.3, 0.4])

    def test_to_tlwh(self):
        """Test the to_tlwh method."""
        self.assertListEqual(
            self.bbox.to_tlwh(),
            [self.bbox.left, self.bbox.top, self.bbox.width, self.bbox.height],
        )

    def test_to_norm_tlwh(self):
        """Test the to_norm_tlwh method."""
        self.assertListEqual(self.bbox.to_norm_tlwh(101, 101), [0.1, 0.2, 0.3, 0.4])

    def test_to_cwh(self):
        """Test the to_cwh method."""
        self.assertListEqual(
            self.bbox.to_cwh(),
            [*self.bbox.center, self.bbox.width, self.bbox.height],
        )

    def test_to_norm_cwh(self):
        """Test the to_norm_cwh method."""
        self.assertListEqual(self.bbox.to_norm_cwh(101, 101), [0.2, 0.3, 0.2, 0.2])

    def test_to_polygon(self):
        """Test the to_polygon method."""
        self.assertListEqual(
            self.bbox.to_polygon(),
            [
                (self.bbox.left, self.bbox.top),
                (self.bbox.right, self.bbox.top),
                (self.bbox.right, self.bbox.bottom),
                (self.bbox.left, self.bbox.bottom),
            ],
        )

    def test_to_alias_methods(self):
        """Test that alias methods are correctly set."""
        self.assertEqual(Bbox.to_pascal_voc, Bbox.to_tlbr)
        self.assertEqual(Bbox.to_xyxy, Bbox.to_tlbr)
        self.assertEqual(Bbox.to_list, Bbox.to_tlbr)
        self.assertEqual(Bbox.to_albu, Bbox.to_norm_tlbr)
        self.assertEqual(Bbox.to_coco, Bbox.to_tlwh)
        self.assertEqual(Bbox.to_yolo, Bbox.to_norm_cwh)

    # end region

    # region Transformations
    def test_shift(self):
        """Test the shift method."""
        shifted_box = self.bbox.shift(horizontal_shift=5, vertical_shift=10)

        self.assertEqual(
            shifted_box,
            Bbox(
                self.bbox.left + 5,
                self.bbox.top + 10,
                self.bbox.right + 5,
                self.bbox.bottom + 10,
            ),
        )

    def test_scale(self):
        """Test the scale method."""
        bbox = Bbox(100, 120, 200, 140)
        self.assertEqual(bbox.scale(2), Bbox(50, 110, 250, 150))

        # Test collapse at center
        cx, cy = bbox.center
        self.assertEqual(bbox.scale(0), Bbox(cx, cy, cx, cy))

        # Test error with negative value
        with self.assertRaises(ValueError):
            bbox.scale(-1)

    def test_expand_uniform(self):
        """Test the expand_uniform method."""
        self.assertEqual(
            self.bbox.expand_uniform(5),
            Bbox(
                self.bbox.left - 5,
                self.bbox.top - 5,
                self.bbox.right + 5,
                self.bbox.bottom + 5,
            ),
        )

    def test_expand(self):
        """Test the expand method."""
        self.assertEqual(self.bbox.expand(5, 10, 15, 20), Bbox(5, 10, 45, 60))

    def test_pad_to_square(self):
        """Test the pad_to_square method."""
        bbox = Bbox(0, 10, 100, 30)
        self.assertEqual(bbox.pad_to_square(), Bbox(0, -30, 100, 70))

        bbox = Bbox(-10, 0, 10, 50)
        self.assertEqual(bbox.pad_to_square(), Bbox(-25, 0, 25, 50))

        # Assert that pad to square returns a copy when the bbox is already square
        bbox = Bbox(0, 0, 10, 10)
        padded = bbox.pad_to_square()
        self.assertEqual(bbox, padded)
        self.assertIsNot(bbox, padded)

    def test_pad_to_aspect_ratio(self):
        """Test the pad_to_aspect_ratio method."""
        bbox = Bbox(0, 10, 100, 30)
        self.assertEqual(bbox.pad_to_aspect_ratio(0.5), Bbox(0, -80, 100, 120))
        self.assertEqual(bbox.pad_to_aspect_ratio(2), Bbox(0, -5, 100, 45))

        bbox = Bbox(10, 0, 30, 100)
        self.assertEqual(bbox.pad_to_aspect_ratio(0.5), Bbox(-5, 0, 45, 100))
        self.assertEqual(bbox.pad_to_aspect_ratio(2), Bbox(-80, 0, 120, 100))

        # Assert that pad to square returns a copy when the bbox is already at the target ratio
        bbox = Bbox(0, 0, 20, 10)
        padded = bbox.pad_to_aspect_ratio(2)
        self.assertEqual(bbox, padded)
        self.assertIsNot(bbox, padded)

        with self.assertRaises(ValueError):
            bbox.pad_to_aspect_ratio(0)

        with self.assertRaises(ValueError):
            bbox.pad_to_aspect_ratio(-10)

    def test_clip_to_img(self):
        """Test the clip_to_img method."""
        # Test no change
        self.assertEqual(self.bbox.clip_to_img(100, 100), self.bbox)

        # Test clipping
        self.assertEqual(self.bbox.clip_to_img(16, 26), Bbox(10, 20, 15, 25))

    def test_overlaps(self):
        """Test the overlaps method."""
        # Test with overlapping bboxes
        bbox1 = Bbox(10, 10, 30, 30)
        bbox2 = Bbox(20, 20, 40, 40)
        self.assertTrue(self.bbox.overlaps(bbox1))
        self.assertTrue(self.bbox.overlaps(bbox2))

        # Test with non-overlapping bboxes
        bbox3 = Bbox(40, 40, 60, 60)
        self.assertFalse(bbox1.overlaps(bbox3), bbox3)

        # Test with identical bboxes
        self.assertTrue(self.bbox.overlaps(self.bbox))

        # Test with bbox inside another bbox
        bbox4 = Bbox(15, 15, 25, 25)
        self.assertEqual(bbox1.union(bbox4), bbox1)

        # Check that two bboxes that share an edge are not overlapping
        self.assertFalse(Bbox(0, 10, 10, 20).overlaps(Bbox(10, 0, 30, 40)))

        # Check that two bboxes that share a single point are not overlapping
        self.assertFalse(Bbox(0, 10, 10, 20).overlaps(Bbox(10, 20, 30, 40)))

        # Test with one bbox with zero width or height
        bbox12 = Bbox(20, 15, 20, 30)
        bbox13 = Bbox(15, 20, 30, 20)
        bbox14 = Bbox(15, 15, 15, 15)
        self.assertFalse(bbox1.overlaps(bbox12))
        self.assertFalse(bbox1.overlaps(bbox13))
        self.assertFalse(bbox1.overlaps(bbox14))

    def test_contains_point(self):
        """Test the contains_point method."""
        self.assertTrue(self.bbox.contains_point(20, 30))
        self.assertFalse(self.bbox.contains_point(5, 15))

        # Check that corners are in:
        for x, y in self.bbox.to_polygon():
            self.assertTrue(self.bbox.contains_point(x, y))

    def test_union(self):
        """Test Bbox union."""
        # Test with overlapping bboxes
        bbox1 = Bbox(10, 10, 30, 30)
        bbox2 = Bbox(20, 20, 40, 40)
        self.assertEqual(bbox1.union(bbox2), Bbox(10, 10, 40, 40))

        # Test with non-overlapping bboxes
        bbox3 = Bbox(40, 40, 60, 60)
        self.assertEqual(bbox1.union(bbox3), Bbox(10, 10, 60, 60))

        # Test with identical bboxes
        self.assertEqual(bbox1.union(bbox1), bbox1)

        # Test with bbox inside another bbox
        bbox4 = Bbox(15, 15, 25, 25)
        self.assertEqual(bbox1.union(bbox4), bbox1)

        # Test with bbox containing another bbox
        bbox5 = Bbox(5, 5, 35, 35)
        self.assertEqual(bbox5.union(bbox1), bbox5)

        # Test with bboxes touching each other
        bbox6 = Bbox(30, 10, 50, 30)
        self.assertEqual(bbox1.union(bbox6), Bbox(10, 10, 50, 30))

        bbox7 = Bbox(10, 30, 30, 50)
        self.assertEqual(bbox1.union(bbox7), Bbox(10, 10, 30, 50))

        # Test with bboxes not touching each other
        bbox8 = Bbox(35, 10, 55, 30)
        self.assertEqual(bbox1.union(bbox8), Bbox(10, 10, 55, 30))

        bbox9 = Bbox(10, 35, 30, 55)
        self.assertEqual(bbox1.union(bbox9), Bbox(10, 10, 30, 55))

        # Test with bboxes with negative coordinates
        bbox10 = Bbox(-10, -10, 10, 10)
        bbox11 = Bbox(-5, -5, 5, 5)
        self.assertEqual(bbox10.union(bbox11), bbox10)

        # Test with bboxes with zero width or height
        bbox12 = Bbox(10, 10, 10, 30)
        bbox13 = Bbox(10, 20, 30, 20)
        self.assertEqual(bbox12.union(bbox13), Bbox(10, 10, 30, 30))

    def test_intersection(self):
        """Test Bbox intersection."""
        # Test with overlapping bboxes
        bbox1 = Bbox(10, 10, 30, 30)
        bbox2 = Bbox(20, 20, 40, 40)
        self.assertEqual(bbox1.intersection(bbox2), Bbox(20, 20, 30, 30))

        # Test with non-overlapping bboxes
        bbox3 = Bbox(40, 40, 60, 60)
        self.assertIsNone(bbox1.intersection(bbox3))

        # Test with identical bboxes
        self.assertEqual(bbox1.intersection(bbox1), bbox1)

        # Test with bbox inside another bbox
        bbox4 = Bbox(15, 15, 25, 25)
        self.assertEqual(bbox1.intersection(bbox4), bbox4)

        # Test with bbox containing another bbox
        bbox5 = Bbox(5, 5, 35, 35)
        self.assertEqual(bbox5.intersection(bbox1), bbox1)

        # Test with bboxes overlapping
        bbox6 = Bbox(30, 10, 50, 30)
        self.assertEqual(bbox1.intersection(bbox6), Bbox(30, 10, 30, 30))

        bbox7 = Bbox(10, 30, 30, 50)
        self.assertEqual(bbox1.intersection(bbox7), Bbox(10, 30, 30, 30))

        # Test with bboxes not touching each other
        bbox8 = Bbox(35, 10, 55, 30)
        self.assertIsNone(bbox1.intersection(bbox8))

        bbox9 = Bbox(10, 35, 30, 55)
        self.assertIsNone(bbox1.intersection(bbox9))

        # Test with bboxes with negative coordinates
        bbox10 = Bbox(-10, -10, 10, 10)
        bbox11 = Bbox(-5, -5, 5, 5)
        self.assertEqual(bbox10.intersection(bbox11), bbox11)

        # Test with bboxes with zero width or height
        bbox12 = Bbox(10, 10, 10, 30)
        bbox13 = Bbox(10, 20, 30, 20)
        self.assertEqual(bbox12.intersection(bbox13), Bbox(10, 20, 10, 20))

        # Test with bboxes sharing an edge
        bbox14 = Bbox(30, 10, 50, 20)
        self.assertEqual(bbox1.intersection(bbox14), Bbox(30, 10, 30, 20))

    def test_iou(self):
        # Test that the IoU is 0 when there is no intersection.
        first = Bbox(0, 0, 10, 10)
        second = Bbox(20, 20, 30, 30)
        self.assertEqual(first.iou(second), 0.0)

        # Test that the IoU is 1 when provided with twice the same bbox.
        self.assertEqual(self.bbox.iou(self.bbox), 1.0)

        # Unless given two bboxes with no area (to avoid ZeroDivError)
        self.assertEqual(Bbox(0, 0, 0, 0).iou(Bbox(5, 5, 5, 5)), 0.0)

        # Test that the IoU is calculated correctly for a partial intersection.
        first = Bbox(0, 0, 10, 10)
        second = Bbox(5, 5, 15, 15)
        self.assertEqual(first.iou(second), 25 / 175)

        # Test that the IoU is calculated correctly when the first bbox contains the second.
        first = Bbox(0, 0, 20, 20)
        second = Bbox(5, 5, 15, 15)
        self.assertEqual(first.iou(second), second.area / first.area)

        # Test that the IoU is calculated correctly when the second bbox contains the first.
        first = Bbox(5, 5, 15, 15)
        second = Bbox(0, 0, 20, 20)
        self.assertEqual(first.iou(second), first.area / second.area)

    def test_distance_to_point(self):
        """Test the distance_to_point method."""
        # Test with point inside the bbox
        self.assertEqual(self.bbox.distance_to_point(20, 30), 0.0)

        # Test with point on the bbox edge
        corners = self.bbox.to_polygon()

        for i, first_corner in enumerate(corners):
            x1, y1 = first_corner
            second_corner = corners[i - 1]

            for step in range(11):
                x2, y2 = second_corner
                x3, y3 = x1 + (step * (x2 - x1)) / 10, y1 + (step * (y2 - y1)) / 10

                self.assertEqual(self.bbox.distance_to_point(x3, y3), 0.0)

        # Test with point outside the bbox
        self.assertEqual(self.bbox.distance_to_point(5, 20), 5)
        self.assertEqual(self.bbox.distance_to_point(5, 40), 5)
        self.assertEqual(self.bbox.distance_to_point(10, 15), 5)
        self.assertEqual(self.bbox.distance_to_point(10, 45), 5)
        self.assertEqual(self.bbox.distance_to_point(35, 45), (5**2 + 5**2) ** 0.5)


if __name__ == "__main__":
    unittest.main()
