[Molden Format]
[Atoms] AU
{% for element, number, Z, x, y, z in atoms %} {{ "% 3s"|format(element) }} {{ "%4g"|format(number) }} {{ "%3g"|format(Z) }} {{ "% 3.6f"|format(x) }} {{ "% 3.6f"|format(y) }} {{ "% 3.6f"|format(z) }}
{% endfor %}[5D7F]
[GTO]
{% for key, value in aos_per_atom.items() %}{{ loop.index }} 0{% for ao in value %}
{{ ao.type }} {{ ao.pnum }} 1.00{% for exponent, contract in ao.coeffs %}
{{ "% 1.10E"|format(exponent) }} {{ "% 1.10E"|format(contract) }}
{%- endfor %}
{%- endfor %}

{% endfor %}
[MO]{% for mo in mos %}
Sym= {{ mo.sym }}
Ene= {{ "% .6f"|format(mo.energy) }}
Spin= Alpha
Occup= {{ "% .6f"|format(mo.occ_num) }}{% for coeff in mo.coeffs %}
{{ "%4g"|format(loop.index) }} {{ "% .6f"|format(coeff) }}
{%- endfor %}
{%- endfor %}
