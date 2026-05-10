with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original = html

# Fix 1: Change data-mi18n to data-i18n in the landing page section
# Find the landing page section
landing_start = html.find('id="landing-welcome"')
if landing_start < 0:
    landing_start = html.find('class="page active"')
landing_end = html.find('id="customer-app"', landing_start)
if landing_end < 0:
    landing_end = html.find('<script', landing_start)

landing_section = html[landing_start:landing_end]
print('Landing section length:', len(landing_section))

# Count data-mi18n in landing section
mi18n_count = landing_section.count('data-mi18n')
print('data-mi18n count in landing:', mi18n_count)

# Replace data-mi18n with data-i18n in landing section
landing_fixed = landing_section.replace('data-mi18n', 'data-i18n')
html = html[:landing_start] + landing_fixed + html[landing_end:]

# Count data-mi18n after fix
mi18n_remaining = html[landing_start:landing_start+len(landing_fixed)].count('data-mi18n')
print('After fix:', mi18n_remaining)

# Verify data-i18n count
i18n_count = landing_fixed.count('data-i18n')
print('data-i18n count in landing after fix:', i18n_count)

with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! File written.')
print('Original size:', len(original), 'New size:', len(html))
