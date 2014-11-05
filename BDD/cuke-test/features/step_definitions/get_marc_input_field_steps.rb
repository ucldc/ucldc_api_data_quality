Given(/^that (\S+).xml has field (\S+) and the value is (.+)$/) do |infile, field, value|
    print('INFOO=>', infile, ' field=>', field, ' val=>', value, "\n")
end

When(/^I look at (\S+)$/) do |resultFile|
    print('RESULT FILE=>', resultFile, "\n")
end

Then(/^(\S+) should be (.+)$/) do | jsonpath, value |
    print("\nJSONP=>", jsonpath, " expected value", value, "\n")
    raise "how do I get earlier values?"
end


