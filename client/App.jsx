import React from 'react';


var ContentList = React.createClass({
    render: function() {
        return <div className="container">
            {this.props.threads.map((i) => 
                <div className="row" key={i.link}><a href="{i.link}">{i.title}</a></div>)}
        </div>
    }
});

var test_list = [
    {link: 'hello', title: 'aeraddas'} ,
    {link: 'hello2', title: 'aeraddas'} 
    ];

export default React.createClass({
    render: function() { 
        return <ContentList threads={test_list} />;
    }
});
