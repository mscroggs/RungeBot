import pytest
import interpolator as ip


@pytest.mark.parametrize("xlim", [
    [-1, 1], [2, 3], [0, 1], [4, 10]
])
@pytest.mark.parametrize("n", range(1, 10))
def test_chebyshev_points(xlim, n):
    c = ip.chebyshev_points(n, xlim)
    for p in c:
        assert xlim[0] <= p <= xlim[1]


@pytest.mark.parametrize("xlim", [
    [-1, 1], [2, 3], [0, 1], [4, 10]
])
@pytest.mark.parametrize("n", range(1, 10))
def test_uniform_points(xlim, n):
    c = ip.uniform_points(n, xlim)
    for p in c:
        assert xlim[0] <= p <= xlim[1]
