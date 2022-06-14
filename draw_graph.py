import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import mplcursors as mc
import re

ptrnNrX = re.compile('\dx')
defultMargin = 20.0


def addMul(matchobj):
    txt = matchobj.group(0)
    result = txt[:1] + '*' + txt[1:]
    return result


def fStringCor(txt):
    res = txt.replace(" ", "").replace("X", "x").replace("^", "**")
    test = ptrnNrX.sub(addMul, res)
    return test


def readFirst():
    try:
        # fTxt = 'sin(x)'
        # fTxt = '-2*x + 5'
        # fTxt = '3/2*x**3 + 10*x**2-4*x-4'
        # fTxt = 'x**4 + 2*x**3 - 4'
        # fTxt = 'x^4 + x^2 + 7'
        fTxt = input("Wprowadz 1 funkcje:\n")
        f = sp.sympify(fStringCor(fTxt))
        return f
    except:
        print("Wystąpił błąd. Spróbuj jeszcze raz.")
        return readFirst()


def readSecond():
    try:
        # gTxt = 'cos(x)'
        # gTxt = '-3*x + x**2'
        # gTxt = 'x**3'
        # gTxt = '2*x**3 + 3*x'
        # gTxt = '5x^3 + x'
        gTxt = input("Wprowadz 2 funkcje:\n")
        g = sp.sympify(fStringCor(gTxt))
        return g
    except:
        print("Wystąpił błąd. Spróbuj jeszcze raz.")
        return readSecond()


def pointsProps(points):
    pMin = min(points)
    pMax = max(points)
    pRange = abs(pMax - pMin)
    pMargin = pRange * 0.3 if pRange > defultMargin else defultMargin
    minLim = pMin - pMargin
    maxLim = pMax + pMargin
    return minLim, maxLim


def main():
    f = readFirst()
    g = readSecond()
    c = sp.simplify(f - g)
    solved = sp.solve(c)
    if len(solved) == 0:
        print("nie znaleziono pojedynczych rozwiazan.")
        return

    res = [complex(r).real for r in solved]

    fig, ax = plt.subplots()

    leftLim, rightLim = pointsProps(res)
    x = np.arange(leftLim, rightLim, abs(rightLim - leftLim) * 0.001)
    symbol = sp.symbols('x')

    ff = sp.lambdify(symbol, f)
    fx = [ff(i) for i in x]
    gf = sp.lambdify(symbol, g)
    gx = [gf(i) for i in x]

    px = []
    py = []

    for r in res:
        y = ff(r)
        y1 = gf(r)
        if abs(y - y1) < 10 ** -10:
            px.append(float(r))
            py.append(y)
            print(f"({r}, {y})")

    if len(px) == 0:
        print("nie znaleziono pojedynczych rozwiazan.")
        return

    downLim, upLim = pointsProps(py)
    plt.xlim((leftLim, rightLim))
    plt.ylim((downLim, upLim))

    plt.plot(x, fx, color='lightgreen', zorder=1, label=r"$" + f"{sp.latex(f)}" + r"$")
    plt.plot(x, gx, color='lightskyblue', zorder=1, label=r"$" + f"{sp.latex(g)}" + r"$")

    plt.vlines(px, downLim, py, linestyle="--", color='grey', zorder=2, linewidth=1)
    plt.hlines(py, leftLim, px, linestyle='--', color='grey', zorder=2, linewidth=1)
    sc = ax.scatter(px, py, color='crimson', marker='o', zorder=3)

    cur = mc.cursor(sc, hover=mc.HoverMode.Transient, highlight=True,
                    highlight_kwargs=dict(facecolor="yellow"))

    @cur.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)
        sel.annotation.set_text(f"x = {sel.target[0]:.4f}\ny = {sel.target[1]:.4f}")

    plt.legend()
    plt.show()
    return


if __name__ == '__main__':
    main()
