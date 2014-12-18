require 'json';

Given(/^that (\S+).xml has field (\S+) and the value is (.+)$/) do |infile, field, value|
    @value = value
    #need to change infile to grab of data
    print('INFOO=>', infile, ' field=>', field, ' val=>', value, "\n")
end

When(/^I look at (\S+)$/) do |resultFile|
    print('RESULT FILE=>', resultFile, "\n")
    #need to change open file to grab of live data
    @json_result = JSON.load(File.open(resultFile, "r"))
    print("srcRes title->"+@json_result['sourceResource']['title'].inspect)
    #json read file
    #save json object
end

Then(/^(\S+) should be (.+)$/) do | jsonpath, value |
    print("\nJSONP=>", jsonpath, " expected value", value, "\n")
    found_value = @json_result['sourceResource']['title'].inspect
    print("srcRes title->"+found_value)
end


