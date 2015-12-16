import React from 'react';


var ContentList = React.createClass({
    render: function() {
        return <div>
            {this.props.threads.map((i) => 
                <p><a href="{i.link}">{i.title}</a></p>)}
        </div>
    }
});

var test_list = [
    {link: 'hello', title: 'aeraddas'} ,
    {link: 'hello', title: 'aeraddas'} 
    ];

export default React.createClass({
    render: function() { 
        return <ContentList threads={test_list} />;
    }
});
