# AlphaTester
#### Trading strategies backtesting platform 

Web platform that allows users to create, test, and manage automated trading strategies. Users can define their strategies based on various technical indicators and risk management parameters, while simulating performance and exchange fees for multiple financial instruments. 

# DISCLAIMER: Past performance does not guarantee future results

# MOTTO: Any sufficiently advanced technology is indistinguishable from magic.
## - Arthur C. Clarke

-----------------------------------------------------------------------------------
### Diagrams
![ERD2](https://github.com/beingsebi/AlphaTester/assets/40637022/ffc01d5e-1b9e-471f-8fe8-67728e7ec57e)
![mermaid-diagram-2024-06-16-012110](https://github.com/beingsebi/AlphaTester/assets/40637022/2d26a0a8-6ad4-4b2b-ab5a-3378b63a9267)

### AI help
We used chatgpt and github copilot during the development. Here are some of the conversations we had with chatgpt:
* https://chatgpt.com/share/d54a1459-9d93-4db1-9dbd-57f72ac74c3e
* https://chatgpt.com/share/99319408-368c-4471-a8d7-eebc704a1e79
* https://chatgpt.com/share/2593d2de-a6a5-409d-99ec-0a89baafeceb
* https://chatgpt.com/share/59b71d70-1078-4960-8bf7-0d669d7101f7

### Design Patterns
In our project, we have utilized:
- The Factory design pattern for creating [instances of indicators](https://github.com/beingsebi/AlphaTester/blob/master/utils/strategy/indicators/indicatorFactory.py).
- Django's `formset_factory` to generate forms for indicators, as seen in this [code snippet](https://github.com/beingsebi/AlphaTester/blob/master/backtester/forms.py#L50).
- The Model-View-Controller (MVC) architecture, albeit with Django's unique interpretation. In Django's MVC, the Controller is referred to as the View, and the View is known as the Template. The Model remains the same as in traditional MVC. This design pattern aids in separating responsibilities, thereby enhancing the manageability and comprehensibility of the code.


### Source control
Throughout the development process we've used github. Here are some noticeable [pull requests](https://github.com/beingsebi/AlphaTester/pulls?q=is%3Apr+is%3Aclosed) we've made:
* PR https://github.com/beingsebi/AlphaTester/pull/26 fixed a bug
* PR https://github.com/beingsebi/AlphaTester/pull/34 refactored part of the code
* PR https://github.com/beingsebi/AlphaTester/pull/22 implemented the strategy runner
* PR https://github.com/beingsebi/AlphaTester/pull/31 added async functionality for the strategy runner
