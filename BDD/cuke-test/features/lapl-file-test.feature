Feature: Title Check
    Title should be set from the 245, 240 and 242 fields

    Scenario Outline:
        Given that <inputFile> has field <inputXPath> and the value is <inputValue>
        When I look at <outputFile> 
        Then <outputJPath> should be <inputValue>

        Examples:
            | inputFile | inputXPath | inputValue | outputFile | outputJPath |
            | ../testdata/tf9580129n.xml | ./x | Test Title | ../testdata/tf9580129n-couchdb.json | ./sourceResource/title |
            | ../testdata/tf9580129n.xml | ./x | Test X Title | ../testdata/tf9580129n-couchdb.json | ./sourceResource/title |

    Scenario Outline:
        Given that <inputFile> has field <inputXPath> with value <inputValue>
        When I look at <outputFile> 
        Then <outputJPath> should be <inputValue>

        Examples:
            | inputFile | inputXPath | inputValue | outputFile | outputJPath |
            | ../testdata/tf9580129n.xml | ./x | Test Title | ../testdata/tf9580129n-couchdb.json | ./sourceResource/title |
            | ../testdata/tf9580129n.xml | ./x | Test X Title | ../testdata/tf9580129n-couchdb.json | ./sourceResource/title |

